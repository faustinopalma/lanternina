const lightbox = document.querySelector<HTMLDialogElement>(".lightbox");
const enlarged = lightbox?.querySelector<HTMLImageElement>("img");
const closeButton = lightbox?.querySelector<HTMLButtonElement>(".lightbox-close");

function closeLightbox() {
  lightbox?.close();
  enlarged?.removeAttribute("src");
}

document.querySelectorAll<HTMLAnchorElement>("main a").forEach((link) => {
  const image = link.querySelector<HTMLImageElement>(":scope > img");
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