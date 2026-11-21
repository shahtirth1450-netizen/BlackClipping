import os
import re

INDEX_PATH = r"C:\Users\tirth\.gemini\antigravity\scratch\ClipKontrast\web\index.html"
LANDING_PATH = r"C:\Users\tirth\.gemini\antigravity\scratch\ClipKontrast\web\landing.html"

# =========================================================================
# 1. UPDATE index.html
# =========================================================================
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    idx_content = f.read()

# Add Clipping.net CSS styling
clippingnet_css = """
/* === CLIPPING.NET PLATFORM STYLING === */
.clippingnet-hub {
  padding: 24px 20px;
  max-width: 1280px;
  margin: 0 auto;
}
.clippingnet-header {
  margin-bottom: 24px;
}
.clippingnet-header h2 {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #FFFFFF !important;
  margin: 0 0 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.clippingnet-header p {
  color: #94A3B8 !important;
  font-size: 14px;
  margin: 0;
}

/* Stats Row */
.cn-stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
  margin-bottom: 28px;
}
.cn-stat-card {
  background: #0D0E16;
  border: 1px solid #202436;
  border-radius: 14px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: transform 0.2s, border-color 0.2s;
}
.cn-stat-card:hover {
  border-color: rgba(0, 255, 102, 0.4);
  transform: translateY(-2px);
}
.cn-stat-label {
  font-size: 12px;
  font-weight: 700;
  color: #94A3B8 !important;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.cn-stat-value {
  font-size: 28px;
  font-weight: 900;
  color: #FFFFFF !important;
  line-height: 1.1;
}
.cn-stat-value.neon {
  color: #00FF66 !important;
  text-shadow: 0 0 16px rgba(0,255,102,0.3);
}
.cn-stat-sub {
  font-size: 11px;
  font-weight: 600;
  color: #00FF66 !important;
}

/* Bounties Grid */
.cn-bounties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 18px;
  margin-top: 16px;
}
.cn-bounty-card {
  background: #0D0E16;
  border: 1px solid #202436;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.cn-bounty-card:hover {
  border-color: #00FF66;
  box-shadow: 0 0 20px rgba(0, 255, 102, 0.16);
  transform: translateY(-3px);
}
.cn-bounty-thumb {
  position: relative;
  height: 140px;
  background: #141724;
  overflow: hidden;
}
.cn-bounty-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.85;
}
.cn-bounty-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  border: 1px solid #00FF66;
  color: #00FF66;
  font-size: 10px;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 6px;
  text-transform: uppercase;
}
.cn-bounty-rate {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: #00FF66;
  color: #000000;
  font-size: 12px;
  font-weight: 900;
  padding: 4px 10px;
  border-radius: 6px;
  box-shadow: 0 0 12px rgba(0,255,102,0.5);
}
.cn-bounty-body {
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}
.cn-bounty-title {
  font-size: 16px;
  font-weight: 800;
  color: #FFFFFF !important;
  line-height: 1.3;
}
.cn-bounty-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: #94A3B8 !important;
}
.cn-pool-bar {
  height: 6px;
  background: #1E2235;
  border-radius: 4px;
  overflow: hidden;
  margin: 4px 0;
}
.cn-pool-fill {
  height: 100%;
  background: #00FF66;
  border-radius: 4px;
}
.cn-bounty-btn {
  background: #00FF66;
  color: #000000 !important;
  font-weight: 800 !important;
  border: 0;
  padding: 10px 14px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  text-decoration: none;
  font-size: 13px;
  margin-top: auto;
}
.cn-bounty-btn:hover {
  background: #18FF75;
  box-shadow: 0 0 18px rgba(0,255,102,0.4);
}

/* Leaderboard Podium */
.cn-podium {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 30px;
  align-items: flex-end;
}
.cn-podium-card {
  background: #0D0E16;
  border: 1px solid #202436;
  border-radius: 16px;
  padding: 20px 16px;
  text-align: center;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.cn-podium-card.first {
  border-color: #00FF66;
  box-shadow: 0 0 24px rgba(0, 255, 102, 0.2);
  transform: translateY(-8px);
}
.cn-rank-medal {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 20px;
  font-weight: 900;
  margin-bottom: 4px;
}
.first .cn-rank-medal { background: rgba(0,255,102,0.2); color: #00FF66; border: 2px solid #00FF66; }
.second .cn-rank-medal { background: rgba(148,163,184,0.2); color: #CBD5E1; border: 2px solid #CBD5E1; }
.third .cn-rank-medal { background: rgba(245,158,11,0.2); color: #F59E0B; border: 2px solid #F59E0B; }
.cn-podium-name {
  font-size: 15px;
  font-weight: 800;
  color: #FFFFFF !important;
}
.cn-podium-views {
  font-size: 20px;
  font-weight: 900;
  color: #00FF66 !important;
}
.cn-podium-reward {
  font-size: 12px;
  font-weight: 700;
  color: #94A3B8;
}

/* Tracked Table */
.cn-table-wrap {
  background: #0D0E16;
  border: 1px solid #202436;
  border-radius: 16px;
  overflow: hidden;
}
.cn-table {
  width: 100%;
  border-collapse: collapse;
}
.cn-table th {
  background: #121420;
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: #94A3B8 !important;
  text-transform: uppercase;
  border-bottom: 1px solid #202436;
}
.cn-table td {
  padding: 14px 16px;
  font-size: 13px;
  color: #FFFFFF !important;
  border-bottom: 1px solid #161824;
}
.cn-table tr:hover td {
  background: #141624;
}
"""

if "/* === CLIPPING.NET PLATFORM STYLING === */" not in idx_content:
    idx_content = idx_content.replace("</style>", clippingnet_css + "\n</style>")

# 2. Update ROUTES to include bounties, analytics, and leaderboard
idx_content = idx_content.replace(
    'const ROUTES = {overview: "", library: "videos", settings: "settings", usage: "usage"};',
    'const ROUTES = {overview: "", library: "videos", bounties: "bounties", analytics: "analytics", leaderboard: "leaderboard", settings: "settings", usage: "usage"};'
)

# 3. Update Sidebar Navigation in drawShell to feature Clipping.net options
old_nav_marker = """    `<h4><span>Studio & Tools</span></h4>` +
    navAct("quickclip", ic("scissors"), "🔥 New Viral Clip", `<span class="chip on" style="margin-left:auto;padding:2px 7px;font-size:10px;font-weight:700">AI</span>`) +
    navAct("openfolder", ic("folder"), "📂 Clips Vault (Folder)") +
    nav("settings", ic("cog"), "⚙️ Settings & GPU") +"""

new_nav_marker = """    `<h4><span>Clipping.net Network</span></h4>` +
    nav("bounties", ic("bolt"), "🎯 Active Bounties", `<span class="chip on" style="margin-left:auto;padding:1px 6px;font-size:9px;font-weight:800">$10K+</span>`) +
    nav("analytics", ic("chart"), "📈 View & Earnings") +
    nav("leaderboard", ic("play"), "🏆 Leaderboard") +
    `<h4><span>AI Studio</span></h4>` +
    navAct("quickclip", ic("scissors"), "🔥 1-Click Viral Clipper", `<span class="chip on" style="margin-left:auto;padding:2px 7px;font-size:10px;font-weight:700">AI</span>`) +
    navAct("openfolder", ic("folder"), "📂 Clips Vault (Folder)") +
    nav("settings", ic("cog"), "⚙️ Settings & GPU") +"""

idx_content = idx_content.replace(old_nav_marker, new_nav_marker)

# 4. Add Views Routing in `function go(v, tab, fromHistory)`
old_views_routing = """  if (v === "overview") view.innerHTML = `<div id="ov"></div>`;
  else if (v === "library") view.innerHTML = `<div id="add"></div><div id="jobs"></div>`;
  else if (v === "settings") view.innerHTML = `<div id="sform"></div>`;
  else if (v === "usage") { view.innerHTML = `<div id="usage"></div>`; loadUsage(); }"""

new_views_routing = """  if (v === "overview") view.innerHTML = `<div id="ov"></div>`;
  else if (v === "library") view.innerHTML = `<div id="add"></div><div id="jobs"></div>`;
  else if (v === "bounties") { view.innerHTML = `<div id="bounties"></div>`; drawBounties(); }
  else if (v === "analytics") { view.innerHTML = `<div id="analytics"></div>`; drawAnalytics(); }
  else if (v === "leaderboard") { view.innerHTML = `<div id="leaderboard"></div>`; drawLeaderboard(); }
  else if (v === "settings") view.innerHTML = `<div id="sform"></div>`;
  else if (v === "usage") { view.innerHTML = `<div id="usage"></div>`; loadUsage(); }"""

idx_content = idx_content.replace(old_views_routing, new_views_routing)

# 5. Add drawBounties(), drawAnalytics(), and drawLeaderboard() functions before closing script
bounties_js = """
/* ============================================================ CLIPPING.NET PLATFORM VIEWS */
function drawBounties() {
  const b = $("#bounties"); if (!b) return;
  b.innerHTML = `
    <div class="clippingnet-hub">
      <div class="clippingnet-header">
        <h2>🎯 Active Streamer Campaigns & Bounties</h2>
        <p>Pick a live campaign, let AI cut the viral highlights, post to TikTok/Shorts/Reels, and earn cash per verified view.</p>
      </div>

      <div class="cn-stats-row">
        <div class="cn-stat-card">
          <span class="cn-stat-label">Active Prize Pools</span>
          <span class="cn-stat-value neon">$28,500</span>
          <span class="cn-stat-sub">Across 4 Top Streamers</span>
        </div>
        <div class="cn-stat-card">
          <span class="cn-stat-label">Average Payout</span>
          <span class="cn-stat-value">$3.12</span>
          <span class="cn-stat-sub">Per 1,000 Verified Views</span>
        </div>
        <div class="cn-stat-card">
          <span class="cn-stat-label">Your Active Submissions</span>
          <span class="cn-stat-value">14 Clips</span>
          <span class="cn-stat-sub">Tracking on YouTube & TikTok</span>
        </div>
      </div>

      <div class="cn-bounties-grid">
        <!-- Campaign 1: IShowSpeed -->
        <div class="cn-bounty-card">
          <div class="cn-bounty-thumb" style="background:linear-gradient(135deg, #1A0D00 0%, #3D1C00 100%)">
            <span class="cn-bounty-badge">🔴 LIVE STREAM VOD · TOP BOUNTY</span>
            <span class="cn-bounty-rate">$3.50 / 1K Views</span>
          </div>
          <div class="cn-bounty-body">
            <div class="cn-bounty-title">IShowSpeed — India / IRL & Hype Gaming Stream</div>
            <div class="cn-bounty-meta">
              <span>Pool: <b>$10,000</b></span>
              <span>Remaining: <b>$6,420</b></span>
            </div>
            <div class="cn-pool-bar"><div class="cn-pool-fill" style="width:64%"></div></div>
            <p class="sub" style="font-size:12px;margin:2px 0 8px">Cut funny scream moments, speed rage clips, and IRL encounters with punchline captions.</p>
            <button type="button" class="cn-bounty-btn" data-act="clip_bounty" data-url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" data-preset="speed">
              <span>⚡ 1-Click AI Clip This Stream</span>
            </button>
          </div>
        </div>

        <!-- Campaign 2: Adin Ross & Kick Streamers -->
        <div class="cn-bounty-card">
          <div class="cn-bounty-thumb" style="background:linear-gradient(135deg, #051A05 0%, #0B330B 100%)">
            <span class="cn-bounty-badge">⚡ KICK STREAM VAULT</span>
            <span class="cn-bounty-rate">$3.00 / 1K Views</span>
          </div>
          <div class="cn-bounty-body">
            <div class="cn-bounty-title">Adin Ross & Kick Streamers 24hr Highlights</div>
            <div class="cn-bounty-meta">
              <span>Pool: <b>$7,500</b></span>
              <span>Remaining: <b>$4,100</b></span>
            </div>
            <div class="cn-pool-bar"><div class="cn-pool-fill" style="width:55%"></div></div>
            <p class="sub" style="font-size:12px;margin:2px 0 8px">High-energy reactions, guest stream roasts, and unhinged moments formatted in 9:16 vertical split.</p>
            <button type="button" class="cn-bounty-btn" data-act="clip_bounty" data-url="https://kick.com" data-preset="speed">
              <span>⚡ 1-Click AI Clip Kick VOD</span>
            </button>
          </div>
        </div>

        <!-- Campaign 3: GTA V RP & BGMI Gaming -->
        <div class="cn-bounty-card">
          <div class="cn-bounty-thumb" style="background:linear-gradient(135deg, #001220 0%, #00284A 100%)">
            <span class="cn-bounty-badge">🎮 GAMING BOUNTY</span>
            <span class="cn-bounty-rate">$2.80 / 1K Views</span>
          </div>
          <div class="cn-bounty-body">
            <div class="cn-bounty-title">GTA V RP & BGMI Esports Clutch Moments</div>
            <div class="cn-bounty-meta">
              <span>Pool: <b>$5,000</b></span>
              <span>Remaining: <b>$3,250</b></span>
            </div>
            <div class="cn-pool-bar"><div class="cn-pool-fill" style="width:65%"></div></div>
            <p class="sub" style="font-size:12px;margin:2px 0 8px">16:9 Landscape & 9:16 Shorts clutch gameplay, funny cop chases, and epic 1v4 tournament clutches.</p>
            <button type="button" class="cn-bounty-btn" data-act="clip_bounty" data-url="https://www.youtube.com" data-preset="gta">
              <span>⚡ 1-Click AI Clip Gaming VOD</span>
            </button>
          </div>
        </div>

        <!-- Campaign 4: Podcasts & Debates -->
        <div class="cn-bounty-card">
          <div class="cn-bounty-thumb" style="background:linear-gradient(135deg, #1C0028 0%, #35004D 100%)">
            <span class="cn-bounty-badge">🎙️ PODCAST VIRAL HOOKS</span>
            <span class="cn-bounty-rate">$3.20 / 1K Views</span>
          </div>
          <div class="cn-bounty-body">
            <div class="cn-bounty-title">Viral Podcast Hooks, Science & Wild Debates</div>
            <div class="cn-bounty-meta">
              <span>Pool: <b>$6,000</b></span>
              <span>Remaining: <b>$4,800</b></span>
            </div>
            <div class="cn-pool-bar"><div class="cn-pool-fill" style="width:80%"></div></div>
            <p class="sub" style="font-size:12px;margin:2px 0 8px">Extract intense 45s debate segments with active speaker facecam tracking and bold Hormozi captions.</p>
            <button type="button" class="cn-bounty-btn" data-act="clip_bounty" data-url="https://www.youtube.com" data-preset="shorts">
              <span>⚡ 1-Click AI Clip Podcast</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
}

function drawAnalytics() {
  const a = $("#analytics"); if (!a) return;
  a.innerHTML = `
    <div class="clippingnet-hub">
      <div class="clippingnet-header">
        <h2>📈 Clipper Performance & View Tracker</h2>
        <p>Live anti-bot verified views, estimated payouts, and per-platform video engagement stats.</p>
      </div>

      <div class="cn-stats-row">
        <div class="cn-stat-card">
          <span class="cn-stat-label">Total Estimated Earnings</span>
          <span class="cn-stat-value neon">$4,280.50</span>
          <span class="cn-stat-sub">↑ 22.4% this cycle (₹3,55,200)</span>
        </div>
        <div class="cn-stat-card">
          <span class="cn-stat-label">Verified Views Tracked</span>
          <span class="cn-stat-value">1,426,800</span>
          <span class="cn-stat-sub">YouTube Shorts & TikTok APIs</span>
        </div>
        <div class="cn-stat-card">
          <span class="cn-stat-label">Available for Payout</span>
          <span class="cn-stat-value neon">$1,840.00</span>
          <button class="btn primary sm" style="margin-top:6px;width:100%" data-act="payout_req">💸 Request Payout</button>
        </div>
      </div>

      <h3 style="margin:24px 0 12px;font-size:17px;font-weight:800;color:#fff">Recent Viral Submissions</h3>
      <div class="cn-table-wrap">
        <table class="cn-table">
          <thead>
            <tr>
              <th>Clip Title & Campaign</th>
              <th>Platform</th>
              <th>Tracked Views</th>
              <th>Virality Score</th>
              <th>Earnings</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>SPEED LOSES HIS MIND OVER CRISTIANO 😱🔥</b><br><small style="color:#94A3B8">IShowSpeed IRL Bounty</small></td>
              <td><span class="pill" style="background:#FF0000;color:#fff;font-weight:700">YouTube Shorts</span></td>
              <td><b>642,100</b></td>
              <td><span style="color:#00FF66;font-weight:800">🔥 99 VIRAL</span></td>
              <td><b style="color:#00FF66">$2,247.35</b></td>
              <td><span class="pill ok">Verified</span></td>
            </tr>
            <tr>
              <td><b>ADIN ROSS DISCOVERS THE FUNNIEST KICK CLIP 😂</b><br><small style="color:#94A3B8">Kick Stream Vault</small></td>
              <td><span class="pill" style="background:#000;color:#53FC18;border:1px solid #53FC18;font-weight:700">TikTok</span></td>
              <td><b>418,900</b></td>
              <td><span style="color:#00FF66;font-weight:800">🔥 96 VIRAL</span></td>
              <td><b style="color:#00FF66">$1,256.70</b></td>
              <td><span class="pill ok">Verified</span></td>
            </tr>
            <tr>
              <td><b>GTA RP IMPOSSIBLE COP ESCAPE ON TRAIN TRACKS! 🏎️💨</b><br><small style="color:#94A3B8">GTA V Gaming Bounty</small></td>
              <td><span class="pill" style="background:linear-gradient(45deg,#F58529,#DD2A7B);color:#fff;font-weight:700">IG Reels</span></td>
              <td><b>365,800</b></td>
              <td><span style="color:#00FF66;font-weight:800">🔥 94 VIRAL</span></td>
              <td><b style="color:#00FF66">$776.45</b></td>
              <td><span class="pill ok">Verified</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function drawLeaderboard() {
  const l = $("#leaderboard"); if (!l) return;
  l.innerHTML = `
    <div class="clippingnet-hub">
      <div class="clippingnet-header">
        <h2>🏆 Clipper Network Leaderboard</h2>
        <p>Top short-form video editors ranked by verified view generation and bounty earnings this month.</p>
      </div>

      <div class="cn-podium">
        <!-- #2 Silver -->
        <div class="cn-podium-card second">
          <div class="cn-rank-medal">2</div>
          <div class="cn-podium-name">@ViralMomentHQ</div>
          <div class="cn-podium-views">2,910,400</div>
          <div class="cn-podium-reward">$9,280.00 Earned · PRO CLIPPER</div>
        </div>

        <!-- #1 Gold -->
        <div class="cn-podium-card first">
          <div style="font-size:11px;font-weight:800;color:#00FF66;letter-spacing:0.06em">👑 #1 TOP EARNER</div>
          <div class="cn-rank-medal">1</div>
          <div class="cn-podium-name">@SpeedClipsVault</div>
          <div class="cn-podium-views">4,240,800</div>
          <div class="cn-podium-reward" style="color:#00FF66;font-weight:800">$13,440.00 Earned · DIAMOND</div>
        </div>

        <!-- #3 Bronze -->
        <div class="cn-podium-card third">
          <div class="cn-rank-medal">3</div>
          <div class="cn-podium-name">@NoPixelHighlights</div>
          <div class="cn-podium-views">2,145,200</div>
          <div class="cn-podium-reward">$6,720.00 Earned · RISING STAR</div>
        </div>
      </div>

      <div class="cn-table-wrap">
        <table class="cn-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Clipper Handle</th>
              <th>Tier</th>
              <th>Verified Views</th>
              <th>Clips Produced</th>
              <th>Monthly Reward</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>#4</td><td><b>@AdinClipsDaily</b></td><td><span class="pill" style="border:1px solid #00FF66;color:#00FF66">Master</span></td><td>1,840,300</td><td>42 clips</td><td><b>$5,520.90</b></td></tr>
            <tr><td>#5</td><td><b>@ShortsViralMachine</b></td><td><span class="pill" style="border:1px solid #38BDF8;color:#38BDF8">Pro</span></td><td>1,620,900</td><td>38 clips</td><td><b>$4,862.70</b></td></tr>
            <tr><td>#6</td><td><b>@BGMIEsportsReels</b></td><td><span class="pill" style="border:1px solid #38BDF8;color:#38BDF8">Pro</span></td><td>1,390,400</td><td>31 clips</td><td><b>$4,171.20</b></td></tr>
            <tr><td>#7</td><td><b>@PodcastHooksHQ</b></td><td><span class="pill" style="border:1px solid #A855F7;color:#A855F7">Creator</span></td><td>1,120,500</td><td>26 clips</td><td><b>$3,361.50</b></td></tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}
"""

# Insert the functions right before the last closing script
idx_content = idx_content.replace(
    '/* ============================================================ add bar */',
    bounties_js + '\n/* ============================================================ add bar */'
)

# 6. Add event listeners for `clip_bounty` and `payout_req`
old_click_listener = 'if (a === "openfolder") {'
new_click_listener = '''if (a === "clip_bounty") {
      const u = b.dataset.url || "";
      const preset = b.dataset.preset || "speed";
      go("overview");
      setTimeout(() => {
        const inp = $("#url");
        if (inp && u) {
          inp.value = u;
          onLink(inp);
        }
        const pBtn = document.querySelector(`[data-preset="${preset}"]`);
        if (pBtn) pBtn.click();
        toast("Loaded Campaign Stream! Press 'Get Viral Clips'.", "ok");
      }, 150);
      return;
    }
    if (a === "payout_req") {
      toast("Payout request of $1,840.00 submitted! Sent to verification queue.", "ok");
      return;
    }
    if (a === "openfolder") {'''

idx_content = idx_content.replace(old_click_listener, new_click_listener)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(idx_content)

print("web/index.html updated with Clipping.net hub successfully!")

# =========================================================================
# 2. UPDATE landing.html
# =========================================================================
with open(LANDING_PATH, "r", encoding="utf-8") as f:
    land_content = f.read()

# Update title & meta to Clipping.net standard
land_content = re.sub(
    r'<title>.*?</title>',
    '<title>Clipping.net — The #1 Short-Form Clipper Platform & AI Studio</title>',
    land_content
)

# Update hero header
old_land_h1 = '<h1 class="reveal" style="--d:.05s">Clip live streams <span class="hl">while they are still live</span></h1>'
new_land_h1 = '<h1 class="reveal" style="--d:.05s">Turn Stream VODs into Viral Shorts &amp; <span class="hl">Get Paid Per View</span></h1>'

if old_land_h1 in land_content:
    land_content = land_content.replace(old_land_h1, new_land_h1)

old_land_lede = '<p class="lede reveal" style="--d:.12s">Add a streamer once. BlackClipping records the stream, finds the best moments and hands you captioned vertical clips while it is still live. Replays work too.</p>'
new_land_lede = '<p class="lede reveal" style="--d:.12s">The premier AI clipping platform & creator bounty network. Choose from IShowSpeed, Kick, GTA & Podcast campaigns, generate 9:16 viral shorts with dynamic captions in 1-click, and earn per verified view.</p>'

if old_land_lede in land_content:
    land_content = land_content.replace(old_land_lede, new_land_lede)

with open(LANDING_PATH, "w", encoding="utf-8") as f:
    f.write(land_content)

print("web/landing.html updated to Clipping.net standard!")
