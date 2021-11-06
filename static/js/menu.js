const bulb = document.querySelector(".bulb")
const menu = document.querySelector(".menu-navigation")

console.log(bulb)

bulb.addEventListener("click", () => {
    menu.classList.toggle("spread")
})

window.addEventListener("click", (e) => {
    if ((menu.classList.contains("spread")) && (e.target != menu) && (e.target != hamburger)) {
        menu.classList.toggle("spread")
    }
})