using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Threading;
using System.Windows.Forms;

namespace BlackClippingApp
{
    static class Program
    {
        private static Mutex mutex = null;
        private static Process serverProcess = null;
        private static NotifyIcon trayIcon = null;
        private static string appDir = "";
        private static int activePort = 8990;

        private static string GetAppUrl()
        {
            return "http://127.0.0.1:" + activePort + "/app";
        }

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            appDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            Directory.SetCurrentDirectory(appDir);

            // Single instance check
            bool isNewInstance = false;
            mutex = new Mutex(true, "BlackClipping_SingleInstance_Mutex_Active", out isNewInstance);
            if (!isNewInstance)
            {
                // Already running, find the active port and open it
                int existingPort = FindRunningBlackClippingPort();
                if (existingPort > 0)
                {
                    activePort = existingPort;
                    OpenAppWindow();
                }
                return;
            }

            try
            {
                // Check if an existing BlackClipping is already answering on any port
                int runningPort = FindRunningBlackClippingPort();
                if (runningPort > 0)
                {
                    activePort = runningPort;
                }
                else
                {
                    // Find next free port so we never clash with other apps (e.g. myraa-agent on 8765)
                    activePort = FindFirstFreePort(8990, 9100);
                    StartBackendServer(activePort);
                    
                    bool ready = WaitForServerReady(activePort, 25);
                    if (!ready)
                    {
                        MessageBox.Show(
                            "BlackClipping backend is taking longer to start or initial packages are being installed.\n\n" +
                            "Please run 'Start-BlackClipping-Windows.bat' to see real-time progress, then open this app again.",
                            "BlackClipping - Initializing",
                            MessageBoxButtons.OK,
                            MessageBoxIcon.Information
                        );
                        return;
                    }
                }

                // Setup System Tray
                SetupTray();

                // Open App Window
                OpenAppWindow();

                // Run message loop for Tray
                Application.Run();
            }
            finally
            {
                Cleanup();
            }
        }

        private static void SetupTray()
        {
            trayIcon = new NotifyIcon();
            trayIcon.Text = "BlackClipping - 100% Viral AI Clipper";
            
            string iconPath = Path.Combine(appDir, "BlackClipping.ico");
            if (File.Exists(iconPath))
            {
                try { trayIcon.Icon = new Icon(iconPath); } catch { trayIcon.Icon = SystemIcons.Application; }
            }
            else
            {
                trayIcon.Icon = SystemIcons.Application;
            }

            ContextMenu menu = new ContextMenu();
            menu.MenuItems.Add(new MenuItem("Open BlackClipping", (s, e) => OpenAppWindow()));
            menu.MenuItems.Add(new MenuItem("Open Clips & Data Folder", (s, e) => OpenDataFolder()));
            menu.MenuItems.Add(new MenuItem("-"));
            menu.MenuItems.Add(new MenuItem("Exit BlackClipping", (s, e) => ExitApp()));

            trayIcon.ContextMenu = menu;
            trayIcon.Visible = true;
            trayIcon.DoubleClick += (s, e) => OpenAppWindow();
        }

        private static int FindRunningBlackClippingPort()
        {
            for (int p = 8990; p <= 9005; p++)
            {
                if (IsBlackClippingServer(p)) return p;
            }
            return -1;
        }

        private static bool IsBlackClippingServer(int port)
        {
            if (port == 9012 || port == 9013 || port == 8765) return false;
            try
            {
                HttpWebRequest req = (HttpWebRequest)WebRequest.Create("http://127.0.0.1:" + port + "/api/status");
                req.Timeout = 1200;
                req.Method = "GET";
                using (HttpWebResponse resp = (HttpWebResponse)req.GetResponse())
                {
                    if (resp.StatusCode != HttpStatusCode.OK) return false;
                    using (StreamReader reader = new StreamReader(resp.GetResponseStream()))
                    {
                        string body = reader.ReadToEnd();
                        return body.Contains("\"user\"") || body.Contains("\"accounts\"");
                    }
                }
            }
            catch
            {
                return false;
            }
        }

        private static bool IsPortAvailable(int port)
        {
            TcpListener listener = null;
            try
            {
                listener = new TcpListener(IPAddress.Loopback, port);
                listener.Start();
                listener.Stop();
                return true;
            }
            catch
            {
                return false;
            }
            finally
            {
                if (listener != null)
                {
                    try { listener.Stop(); } catch { }
                }
            }
        }

        private static int FindFirstFreePort(int startPort, int endPort)
        {
            for (int p = startPort; p <= endPort; p++)
            {
                if (p == 9012 || p == 9013 || p == 8765) continue;
                if (IsPortAvailable(p)) return p;
            }
            return startPort;
        }

        private static void StartBackendServer(int port)
        {
            string pythonExe = FindPythonExecutable();
            if (string.IsNullOrEmpty(pythonExe))
            {
                MessageBox.Show(
                    "Python was not found on this computer.\nPlease run 'Start-BlackClipping-Windows.bat' first to automatically install Python and setup the environment.",
                    "BlackClipping - Setup Required",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning
                );
                Environment.Exit(1);
                return;
            }

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = pythonExe;
            psi.Arguments = "-m studio.server";
            psi.WorkingDirectory = appDir;
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;
            psi.WindowStyle = ProcessWindowStyle.Hidden;

            // Set environment variables
            psi.EnvironmentVariables["BLACKCLIPPING_PORT"] = port.ToString();
            psi.EnvironmentVariables["CLIPKONTRAST_PORT"] = port.ToString();
            psi.EnvironmentVariables["CLIPKONTRAST_OPEN_BROWSER"] = "0";
            psi.EnvironmentVariables["PYTHONWARNINGS"] = "ignore::DeprecationWarning";

            try
            {
                serverProcess = Process.Start(psi);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to launch BlackClipping backend:\n" + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Environment.Exit(1);
            }
        }

        private static bool WaitForServerReady(int port, int maxSeconds)
        {
            int elapsed = 0;
            while (elapsed < maxSeconds * 2)
            {
                if (IsBlackClippingServer(port)) return true;
                Thread.Sleep(500);
                elapsed++;
            }
            return false;
        }

        private static string FindPythonExecutable()
        {
            // 1. Check local virtual environment
            string venvPy = Path.Combine(appDir, ".venv", "Scripts", "python.exe");
            if (File.Exists(venvPy)) return venvPy;

            venvPy = Path.Combine(appDir, "venv", "Scripts", "python.exe");
            if (File.Exists(venvPy)) return venvPy;

            // 2. Check AppData local python installs
            string localApp = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            string[] knownPaths = new string[]
            {
                Path.Combine(localApp, @"Programs\Python\Python312\python.exe"),
                Path.Combine(localApp, @"Programs\Python\Python311\python.exe"),
                Path.Combine(localApp, @"Programs\Python\Python310\python.exe"),
                @"C:\Python312\python.exe",
                @"C:\Python311\python.exe",
                @"C:\Python310\python.exe"
            };
            foreach (string p in knownPaths)
            {
                if (File.Exists(p)) return p;
            }

            // 3. Check system PATH
            string pathEnv = Environment.GetEnvironmentVariable("PATH") ?? "";
            foreach (string dir in pathEnv.Split(';'))
            {
                string trimmed = dir.Trim();
                if (!string.IsNullOrEmpty(trimmed) && Directory.Exists(trimmed))
                {
                    string cand = Path.Combine(trimmed, "python.exe");
                    if (File.Exists(cand)) return cand;
                }
            }

            return "python.exe";
        }

        public static void OpenAppWindow()
        {
            string url = GetAppUrl();

            // Try Edge App Mode (Frameless dedicated window)
            string edge = @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe";
            if (!File.Exists(edge)) edge = @"C:\Program Files\Microsoft\Edge\Application\msedge.exe";

            string chrome = @"C:\Program Files\Google\Chrome\Application\chrome.exe";
            if (!File.Exists(chrome)) chrome = @"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe";

            if (File.Exists(edge))
            {
                Process.Start(edge, "--app=" + url + " --window-size=1280,820");
                return;
            }
            if (File.Exists(chrome))
            {
                Process.Start(chrome, "--app=" + url + " --window-size=1280,820");
                return;
            }

            // Fallback to default browser
            Process.Start(url);
        }

        private static void OpenDataFolder()
        {
            string dataDir = Path.Combine(appDir, "data");
            if (!Directory.Exists(dataDir)) Directory.CreateDirectory(dataDir);
            Process.Start("explorer.exe", dataDir);
        }

        private static void ExitApp()
        {
            Cleanup();
            if (trayIcon != null)
            {
                trayIcon.Visible = false;
                trayIcon.Dispose();
            }
            Application.Exit();
        }

        private static void Cleanup()
        {
            if (serverProcess != null && !serverProcess.HasExited)
            {
                try
                {
                    serverProcess.Kill();
                }
                catch { }
            }
            if (mutex != null)
            {
                try { mutex.ReleaseMutex(); } catch { }
            }
        }
    }
}
