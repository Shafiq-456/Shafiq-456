<div align="center">

<!-- Night coder SVG animation -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" width="800" height="300">
  <defs>
    <!-- Room background gradient -->
    <linearGradient id="roomGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#0d1117"/>
      <stop offset="100%" style="stop-color:#161b22"/>
    </linearGradient>
    <!-- Window city glow -->
    <linearGradient id="cityGlow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#0a1628"/>
      <stop offset="100%" style="stop-color:#1a2a4a"/>
    </linearGradient>
    <!-- Monitor screen glow -->
    <radialGradient id="screenGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#58a6ff;stop-opacity:0.4"/>
      <stop offset="100%" style="stop-color:#0d1117;stop-opacity:0"/>
    </radialGradient>
    <!-- Lamp glow -->
    <radialGradient id="lampGlow" cx="50%" cy="20%" r="80%">
      <stop offset="0%" style="stop-color:#ffd700;stop-opacity:0.3"/>
      <stop offset="100%" style="stop-color:#ffd700;stop-opacity:0"/>
    </radialGradient>
    <!-- Desk lamp gradient -->
    <linearGradient id="lampShade" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#c9a84c"/>
      <stop offset="100%" style="stop-color:#8b6914"/>
    </linearGradient>
    <!-- City lights flicker animation -->
    <animate id="cityFlicker"/>
    <!-- Typing cursor blink -->
    <style>
      @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
      @keyframes screenPulse { 0%,100%{opacity:0.6} 50%{opacity:1} }
      @keyframes cityLight1 { 0%,100%{opacity:1} 47%{opacity:1} 48%{opacity:0.3} 50%{opacity:1} }
      @keyframes cityLight2 { 0%,100%{opacity:0.7} 30%{opacity:0.7} 31%{opacity:0.2} 33%{opacity:0.7} 80%{opacity:0.7} 81%{opacity:0.1} 83%{opacity:0.7} }
      @keyframes cityLight3 { 0%,100%{opacity:0.9} 60%{opacity:0.9} 61%{opacity:0} 63%{opacity:0.9} }
      @keyframes typing { 0%{width:0} 100%{width:100%} }
      @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-3px)} }
      @keyframes neonPulse { 0%,100%{opacity:0.8;filter:drop-shadow(0 0 4px #58a6ff)} 50%{opacity:1;filter:drop-shadow(0 0 8px #58a6ff)} }
      @keyframes clockTick { 0%{opacity:1} 49%{opacity:1} 50%{opacity:0} 100%{opacity:0} }
      @keyframes codeScroll { 0%{transform:translateY(0)} 100%{transform:translateY(-40px)} }
      @keyframes lampFlicker { 0%,100%{opacity:0.3} 92%{opacity:0.3} 93%{opacity:0.1} 95%{opacity:0.3} 97%{opacity:0.15} 99%{opacity:0.3} }
      @keyframes redDot { 0%,100%{opacity:1} 50%{opacity:0.3} }
    </style>
  </defs>

  <!-- Room background -->
  <rect width="800" height="300" fill="url(#roomGrad)"/>

  <!-- City window (left side) -->
  <rect x="30" y="20" width="220" height="200" rx="4" fill="url(#cityGlow)" stroke="#1e3a5f" stroke-width="2"/>

  <!-- City skyline silhouette -->
  <g fill="#0a1525">
    <rect x="40" y="120" width="20" height="100"/>
    <rect x="55" y="100" width="15" height="120"/>
    <rect x="68" y="80" width="25" height="140"/>
    <rect x="90" y="110" width="18" height="110"/>
    <rect x="105" y="90" width="30" height="130"/>
    <rect x="130" y="105" width="20" height="115"/>
    <rect x="145" y="70" width="22" height="150"/>
    <rect x="162" y="95" width="16" height="125"/>
    <rect x="175" y="85" width="28" height="135"/>
    <rect x="198" y="100" width="22" height="120"/>
    <rect x="215" y="115" width="25" height="105"/>
  </g>

  <!-- City lights (windows in buildings) - animated -->
  <g style="animation:cityLight1 7s infinite">
    <rect x="58" y="108" width="4" height="3" fill="#ffd700" opacity="0.9"/>
    <rect x="64" y="115" width="4" height="3" fill="#87ceeb" opacity="0.8"/>
    <rect x="72" y="95" width="4" height="3" fill="#ffd700" opacity="0.7"/>
    <rect x="80" y="100" width="4" height="3" fill="#ff9966" opacity="0.8"/>
  </g>
  <g style="animation:cityLight2 5s infinite">
    <rect x="108" y="97" width="4" height="3" fill="#87ceeb" opacity="0.9"/>
    <rect x="115" y="104" width="4" height="3" fill="#ffd700" opacity="0.8"/>
    <rect x="122" y="112" width="4" height="3" fill="#ffd700" opacity="0.6"/>
    <rect x="148" y="78" width="4" height="3" fill="#ff9966" opacity="0.7"/>
    <rect x="155" y="90" width="4" height="3" fill="#87ceeb" opacity="0.9"/>
  </g>
  <g style="animation:cityLight3 9s infinite">
    <rect x="178" y="93" width="4" height="3" fill="#ffd700" opacity="0.8"/>
    <rect x="185" y="100" width="4" height="3" fill="#87ceeb" opacity="0.7"/>
    <rect x="200" y="108" width="4" height="3" fill="#ffd700" opacity="0.9"/>
    <rect x="218" y="120" width="4" height="3" fill="#ff9966" opacity="0.8"/>
  </g>

  <!-- Moon -->
  <circle cx="210" cy="45" r="18" fill="#e8e0c8" opacity="0.9"/>
  <circle cx="218" cy="40" r="13" fill="url(#cityGlow)" opacity="0.95"/>

  <!-- Stars -->
  <circle cx="55" cy="35" r="1.2" fill="white" opacity="0.8"/>
  <circle cx="90" cy="28" r="0.8" fill="white" opacity="0.6"/>
  <circle cx="130" cy="40" r="1" fill="white" opacity="0.7"/>
  <circle cx="160" cy="32" r="1.5" fill="white" opacity="0.5"/>
  <circle cx="175" cy="50" r="0.9" fill="white" opacity="0.8"/>

  <!-- Desk -->
  <rect x="220" y="200" width="560" height="15" rx="2" fill="#2d1b00" stroke="#3d2800" stroke-width="1"/>
  <rect x="220" y="213" width="10" height="60" fill="#1a0f00"/>
  <rect x="770" y="213" width="10" height="60" fill="#1a0f00"/>

  <!-- Shelf on wall -->
  <rect x="480" y="40" width="200" height="8" rx="2" fill="#2d1b00"/>
  <!-- Books on shelf -->
  <rect x="490" y="20" width="12" height="22" rx="1" fill="#c0392b"/>
  <rect x="504" y="24" width="10" height="18" rx="1" fill="#2980b9"/>
  <rect x="516" y="22" width="14" height="20" rx="1" fill="#27ae60"/>
  <rect x="532" y="26" width="10" height="16" rx="1" fill="#8e44ad"/>
  <rect x="544" y="20" width="12" height="22" rx="1" fill="#e67e22"/>
  <!-- Plant on shelf -->
  <rect x="640" y="30" width="8" height="12" rx="1" fill="#5d4037"/>
  <ellipse cx="644" cy="28" rx="12" ry="10" fill="#2d6a4f"/>
  <ellipse cx="638" cy="22" rx="8" ry="7" fill="#40916c"/>
  <ellipse cx="652" cy="24" rx="9" ry="7" fill="#52b788"/>

  <!-- Monitor stand -->
  <rect x="380" y="170" width="8" height="32" fill="#30363d"/>
  <rect x="360" y="198" width="48" height="6" rx="2" fill="#30363d"/>

  <!-- Monitor -->
  <rect x="290" y="100" width="188" height="72" rx="6" fill="#161b22" stroke="#30363d" stroke-width="2"/>
  <!-- Screen content -->
  <rect x="295" y="105" width="178" height="62" rx="4" fill="#0d1117"/>
  <!-- Screen glow effect -->
  <rect x="295" y="105" width="178" height="62" rx="4" fill="url(#screenGlow)" style="animation:screenPulse 3s ease-in-out infinite"/>

  <!-- Code on screen -->
  <g style="animation:codeScroll 8s linear infinite">
    <text x="302" y="122" font-family="'Courier New', monospace" font-size="7" fill="#58a6ff">const shafiq = {</text>
    <text x="308" y="131" font-family="'Courier New', monospace" font-size="7" fill="#79c0ff">  role: <tspan fill="#a5d6ff">"Full Stack Dev"</tspan>,</text>
    <text x="308" y="140" font-family="'Courier New', monospace" font-size="7" fill="#79c0ff">  passion: <tspan fill="#a5d6ff">"Building"</tspan>,</text>
    <text x="308" y="149" font-family="'Courier New', monospace" font-size="7" fill="#79c0ff">  status: <tspan fill="#3fb950">"online"</tspan></text>
    <text x="302" y="158" font-family="'Courier New', monospace" font-size="7" fill="#58a6ff">};</text>
  </g>

  <!-- Cursor blink on screen -->
  <rect x="302" y="158" width="5" height="8" fill="#58a6ff" style="animation:blink 1s step-end infinite"/>

  <!-- Clock/LED display (top right of desk area) -->
  <rect x="600" y="55" width="70" height="30" rx="3" fill="#0d0d0d" stroke="#333" stroke-width="1"/>
  <text x="613" y="76" font-family="'Courier New', monospace" font-size="18" fill="#ff4444" font-weight="bold" style="animation:neonPulse 2s ease-in-out infinite">01:17</text>

  <!-- Desk lamp -->
  <rect x="530" y="165" width="4" height="38" fill="#555" transform="rotate(-8,532,203)"/>
  <ellipse cx="516" cy="162" rx="22" ry="10" fill="url(#lampShade)" transform="rotate(-15,516,162)"/>
  <ellipse cx="516" cy="162" rx="16" ry="6" fill="#ffd700" opacity="0.6" style="animation:lampFlicker 10s infinite"/>
  <!-- Lamp light cone -->
  <polygon points="500,170 535,170 555,200 480,200" fill="#ffd700" opacity="0.04" style="animation:lampFlicker 10s infinite"/>
  <rect x="533" y="200" width="6" height="4" rx="1" fill="#444"/>

  <!-- Coffee mug -->
  <rect x="560" y="183" width="22" height="18" rx="3" fill="#3d2b1f" stroke="#555" stroke-width="1"/>
  <path d="M582,189 Q590,189 590,196 Q590,203 582,203" stroke="#555" stroke-width="2" fill="none"/>
  <!-- Steam from coffee -->
  <path d="M566,180 Q568,174 566,170" stroke="#aaa" stroke-width="1.5" fill="none" opacity="0.5" style="animation:float 2s ease-in-out infinite"/>
  <path d="M572,182 Q574,175 572,170" stroke="#aaa" stroke-width="1.5" fill="none" opacity="0.4" style="animation:float 2s ease-in-out infinite 0.5s"/>

  <!-- Headphones on desk -->
  <path d="M620,195 Q640,175 660,195" stroke="#58a6ff" stroke-width="3" fill="none"/>
  <rect x="617" y="192" width="7" height="10" rx="3" fill="#30363d" stroke="#58a6ff" stroke-width="1"/>
  <rect x="657" y="192" width="7" height="10" rx="3" fill="#30363d" stroke="#58a6ff" stroke-width="1"/>

  <!-- Person (coder) sitting -->
  <!-- Chair -->
  <rect x="350" y="215" width="70" height="8" rx="3" fill="#1a1a2e"/>
  <rect x="415" y="215" width="6" height="50" fill="#0f0f1a"/>
  <rect x="350" y="215" width="6" height="50" fill="#0f0f1a"/>
  <rect x="360" y="175" width="8" height="45" rx="2" fill="#1a1a2e"/>
  <!-- Body -->
  <rect x="358" y="155" width="35" height="28" rx="8" fill="#1e3a5f"/>
  <!-- Head -->
  <circle cx="375" cy="145" r="16" fill="#c49a6c"/>
  <!-- Hair -->
  <path d="M360,138 Q375,125 390,138" fill="#1a0a00"/>
  <ellipse cx="375" cy="132" rx="16" ry="8" fill="#1a0a00"/>
  <!-- Arms -->
  <path d="M358,163 Q340,172 330,180" stroke="#c49a6c" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M393,163 Q408,172 418,180" stroke="#c49a6c" stroke-width="8" fill="none" stroke-linecap="round"/>

  <!-- Keyboard -->
  <rect x="300" y="200" width="120" height="8" rx="3" fill="#21262d" stroke="#30363d" stroke-width="1"/>
  <!-- Keyboard keys hint -->
  <rect x="306" y="202" width="6" height="4" rx="1" fill="#30363d"/>
  <rect x="315" y="202" width="6" height="4" rx="1" fill="#30363d"/>
  <rect x="324" y="202" width="6" height="4" rx="1" fill="#30363d"/>
  <rect x="333" y="202" width="20" height="4" rx="1" fill="#30363d"/>
  <rect x="356" y="202" width="6" height="4" rx="1" fill="#30363d"/>
  <rect x="365" y="202" width="6" height="4" rx="1" fill="#30363d"/>
  <rect x="374" y="202" width="6" height="4" rx="1" fill="#30363d"/>
  <rect x="383" y="202" width="20" height="4" rx="1" fill="#58a6ff"/>

  <!-- Mouse -->
  <rect x="430" y="198" width="20" height="10" rx="5" fill="#21262d" stroke="#30363d" stroke-width="1"/>
  <line x1="440" y1="198" x2="440" y2="203" stroke="#30363d" stroke-width="1"/>

  <!-- Red notification dots (like in original) -->
  <circle cx="720" cy="130" r="8" fill="#ff4d4d" style="animation:redDot 2s ease-in-out infinite"/>
  <circle cx="720" cy="150" r="8" fill="#ff4d4d" style="animation:redDot 2s ease-in-out infinite 0.5s"/>
  <circle cx="720" cy="170" r="8" fill="#ff4d4d" style="animation:redDot 2s ease-in-out infinite 1s"/>

  <!-- Ambient room glow from monitor -->
  <rect x="280" y="95" width="210" height="115" rx="10" fill="#58a6ff" opacity="0.03" style="animation:screenPulse 3s ease-in-out infinite"/>

  <!-- Floor shadow under desk -->
  <ellipse cx="550" cy="270" rx="300" ry="15" fill="#000" opacity="0.3"/>

  <!-- Small plant on desk -->
  <rect x="740" y="186" width="12" height="16" rx="2" fill="#5d4037"/>
  <ellipse cx="746" cy="184" rx="14" ry="12" fill="#2d6a4f" opacity="0.9"/>
  <ellipse cx="740" cy="178" rx="9" ry="8" fill="#40916c"/>
  <ellipse cx="753" cy="179" rx="10" ry="8" fill="#52b788"/>
</svg>

<br/>

<!-- Animated typing header -->
<a href="https://github.com/Shafiq-456">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&pause=1000&color=58A6FF&center=true&vCenter=true&width=700&lines=Hey+there!+I'm+Shafiq+%F0%9F%91%8B;Full+Stack+Developer+%F0%9F%9A%80;Flutter+%7C+TypeScript+%7C+JavaScript;Always+coding...+always+learning+%F0%9F%92%BB" alt="Typing SVG" />
</a>

<br/><br/>

<!-- Badges row -->
[![Profile Views](https://komarev.com/ghpvc/?username=Shafiq-456&color=58a6ff&style=for-the-badge&label=PROFILE+VIEWS)](https://github.com/Shafiq-456)
[![GitHub followers](https://img.shields.io/github/followers/Shafiq-456?style=for-the-badge&color=58a6ff&logo=github)](https://github.com/Shafiq-456?tab=followers)
[![GitHub stars](https://img.shields.io/github/stars/Shafiq-456?style=for-the-badge&color=ffd700&logo=github)](https://github.com/Shafiq-456)

</div>

---

## 🧑‍💻 About Me

```typescript
const shafiq = {
  username   : "Shafiq-456",
  role       : "Full Stack Developer",
  languages  : ["TypeScript", "JavaScript", "Dart", "Python"],
  frameworks : ["Flutter", "React", "Node.js"],
  currentWork: "Building impactful projects — one commit at a time 🚀",
  interests  : ["Web Dev", "Mobile Apps", "QA Testing", "AI Tools"],
  funFact    : "I debug with coffee ☕ and solve bugs past midnight 🌙",
};
```

---

## 🚀 Tech Stack

<div align="center">

### 💻 Languages
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Dart](https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### 🛠️ Frameworks & Tools
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-0078d7?style=for-the-badge&logo=visual-studio-code&logoColor=white)

### 🧪 QA & Testing
![Manual Testing](https://img.shields.io/badge/Manual%20Testing-FF6B6B?style=for-the-badge&logo=testcafe&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

</div>

---

## 📊 GitHub Stats

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=Shafiq-456&show_icons=true&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=c9d1d9&rank_icon=github" width="48%" alt="GitHub Stats"/>
  <img src="https://github-readme-streak-stats.herokuapp.com?user=Shafiq-456&theme=github-dark-blue&hide_border=true&background=0d1117&stroke=30363d&ring=58a6ff&fire=ff6b35&currStreakLabel=58a6ff" width="48%" alt="GitHub Streak"/>
</div>

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Shafiq-456&layout=compact&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9" width="40%" alt="Top Languages"/>
</div>

---

## 🔥 Featured Projects

| Project | Description | Stack |
|--------|-------------|-------|
| [🏢 Grace Impex Portfolio](https://github.com/Shafiq-456/grace-impex-portfolio) | Professional business portfolio site | TypeScript |
| [🤖 JeduAI App](https://github.com/Shafiq-456/JeduAI-App) | AI-powered education mobile app | Flutter / Dart |
| [💼 SmartBiz ERP](https://github.com/Shafiq-456/SmartBiz-ERP) | Business management ERP system | JavaScript |
| [✅ GPay QA Portfolio](https://github.com/Shafiq-456/GPay-QA-Portfolio) | Manual QA testing for Google Pay | QA Testing |
| [💡 BrightPath](https://github.com/Shafiq-456/BrightPath) | Learning & growth platform | — |

---

## 🌐 Connect With Me

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Shafiq--456-181717?style=for-the-badge&logo=github)](https://github.com/Shafiq-456)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/your-linkedin)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail)](mailto:your@email.com)

</div>

---

<div align="center">

<!-- Activity graph -->
[![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=Shafiq-456&theme=github-compact&bg_color=0d1117&color=58a6ff&line=58a6ff&point=ffffff&hide_border=true)](https://github.com/Shafiq-456)

<br/>

*"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."*
— Martin Fowler

<br/>

![Wave](https://raw.githubusercontent.com/mayhemantt/mayhemantt/Update/svg/Bottom.svg)

</div>
