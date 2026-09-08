const lightbox = document.querySelector(".lightbox");
const enlarged = lightbox?.querySelector("img");
const closeButton = lightbox?.querySelector(".lightbox-close");

function closeLightbox() {
  lightbox?.close();
  enlarged?.removeAttribute("src");
}

document.querySelectorAll("main a").forEach((link) => {
  const image = link.querySelector(":scope > img");
  if (!image) return;
  image.classList.add("zoomable");
  image.addEventListener("click", (event) => {
    event.preventDefault();
    if (!lightbox || !enlarged) return;
    enlarged.src = link.href;
    enlarged.alt = image.alt;
    lightbox.showModal();
  });
});

closeButton?.addEventListener("click", closeLightbox);
enlarged?.addEventListener("click", closeLightbox);
lightbox?.addEventListener("click", (event) => {
  if (event.target === lightbox) closeLightbox();
});
lightbox?.addEventListener("close", () => enlarged?.removeAttribute("src"));