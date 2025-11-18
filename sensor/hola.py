async function bypassTeasers() {
    try {
        const token = localStorage.getItem("TinderWeb/APIToken");
        
        if (!token) {
            console.log("Token não encontrado");
            return;
        }

        const response = await fetch("https://api.gotinder.com/v2/fast-match/teasers", {
            headers: {
                "X-Auth-Token": token,
                "platform": "android"
            }
        });

        if (!response.ok) {
            console.error("Erro ao buscar teasers:", response.status);
            return;
        }

        const teasers = (await response.json())?.data?.results || [];
        const elements = document.querySelectorAll(".Expand.enterAnimationContainer > div:nth-child(1)");

        teasers.forEach((teaser, i) => {
            const el = elements[i];
            if (!el) return;

            const name = teaser.user?.name || "Unknown";
            const birthDate = teaser.user?.birth_date;
            const age = birthDate ? Math.floor((new Date() - new Date(birthDate)) / (365.25 * 24 * 60 * 60 * 1000)) : "N/A";
            const photoUrl = teaser.user?.photos?.[0]?.processedFiles?.[0]?.url;

            if (!photoUrl) return;

            el.style.backgroundImage = `url(${photoUrl})`;
            el.style.backgroundSize = "cover";
            el.style.filter = "none";
            el.style.backdropFilter = "none";
            el.textContent = `${name}, ${age}`;
            el.style.color = "white";
            el.style.textShadow = "2px 2px 4px black";
            el.style.fontWeight = "bold";
            el.style.fontSize = "16px";
            el.style.padding = "10px";
            el.style.display = "flex";
            el.style.alignItems = "flex-end";
        });
    } catch (error) {
        console.error("Erro:", error);
    }
}

bypassTeasers();
setInterval(bypassTeasers, 3000);

async function bypassTeasers() { try { const token = localStorage.getItem("TinderWeb/APIToken"); if (!token) { console.log("Token não encontrado"); return; }const response = await fetch("https://api.gotinder.com/v2/fast-match/teasers", {
  headers: { "X-Auth-Token": token, "platform": "android" }
});

if (!response.ok) {
  console.error("Erro ao buscar teasers:", response.status);
  return;
}

const teasers = (await response.json())?.data?.results || [];
const elements = document.querySelectorAll(".Expand.enterAnimationContainer > div:nth-child(1)");

teasers.forEach((teaser, i) => {
  const el = elements[i];
  if (!el) return;

  const name = teaser.user?.name || "Unkown";
  const birthDate = teaser.user?.birth_date;
  const age = birthDate ? Math.floor((new Date() - new Date(birthDate)) / (365.25 * 24 * 60 * 60 * 1000)) : "N/A";

  const photoUrl = teaser.user?.photos[0]?.processedFiles?.[0]?.url;
  if (!photoUrl) return;

  el.style.backgroundImage = `url(${photoUrl})`;
  el.style.backgroundSize = "cover";
  el.style.backgroundPosition = "center";
  el.style.color = "white";
  el.style.fontSize = "18px";
  el.style.textShadow = "2px 2px 4px black";
  el.innerHTML = `${name}, ${age}`;
  el.style.display = "flex";
  el.style.alignItems = "flex-end";
  el.style.justifyContent = "flex-end";
  el.style.padding = "10px";
});
} catch (error) { console.error("Erro:", error); } }

bypassTeasers(); setInterval(bypassTeasers, 3000);
