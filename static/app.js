document.addEventListener("DOMContentLoaded", () => {
  const postEl = document.getElementById("post");
  const btn = document.getElementById("generate");
  const clearBtn = document.getElementById("clear");
  const tagsEl = document.getElementById("tags");
  const countEl = document.getElementById("count");
  const toast = document.getElementById("toast");
  const copyAllBtn = document.getElementById("copyAll");

  function showToast(msg) {
    toast.innerText = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2200);
  }

  async function generate() {
    const text = postEl.value.trim();
    const top_n = parseInt(countEl.value) || 8;
    if (!text) {
      showToast("Please enter some text first.");
      return;
    }

    tagsEl.innerHTML = '<p class="placeholder">Generating...</p>';
    btn.disabled = true;
    try {
      const resp = await fetch("/api/hashtags", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, top_n }),
      });
      if (!resp.ok) throw new Error("Server error");
      const data = await resp.json();
      renderTags(data.hashtags || []);
    } catch (err) {
      tagsEl.innerHTML = `<p class="placeholder">Error: ${err.message}</p>`;
    } finally {
      btn.disabled = false;
    }
  }

  function renderTags(tags) {
    tagsEl.innerHTML = "";
    if (tags.length === 0) {
      tagsEl.innerHTML = '<p class="placeholder">No hashtags found.</p>';
      return;
    }
    tags.forEach((t) => {
      const tag = document.createElement("div");
      tag.className = "tag";
      tag.innerText = t;
      const copyBtn = document.createElement("button");
      copyBtn.innerText = "📋";
      copyBtn.title = "Copy hashtag";
      copyBtn.onclick = async () => {
        await navigator.clipboard.writeText(t);
        showToast(`Copied ${t}`);
      };
      tag.appendChild(copyBtn);
      tagsEl.appendChild(tag);
    });
  }

  copyAllBtn.onclick = async () => {
    const allTags = Array.from(tagsEl.querySelectorAll(".tag"))
      .map((t) => t.firstChild.textContent)
      .join(" ");
    if (!allTags) return showToast("No hashtags to copy.");
    await navigator.clipboard.writeText(allTags);
    showToast("Copied all hashtags!");
  };

  clearBtn.onclick = () => {
    postEl.value = "";
    tagsEl.innerHTML = '<p class="placeholder">Paste text and click Generate</p>';
  };

  btn.onclick = generate;
});
