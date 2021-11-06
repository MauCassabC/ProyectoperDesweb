const images = document.querySelectorAll(".img-galeria")
const images_light = document.querySelector(".agregar-imagen")
const container_light = document.querySelector("imagen-light")
const hamburger2 = document.querySelector(".bulb")

images.forEach(e => {
    e.addEventListener("click", () => {
        showImage(e.getAttribute("src"))

    })
});

const showImage = (img) => { 
    images_light.src = img
    container_light.classList.toggle("show")
    images_light.classList.toggle("showImage")
    hamburger2.style.opacity = 0;
}

container_light.addEventListener("click", (e) => {
    if (e.target != images_light) {
        container_light.classList.toggle("show")
        images_light.classList.toggle("showImage")
        hamburger2.style.opacity = 1;
    }
})