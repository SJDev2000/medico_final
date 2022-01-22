const sunPath = "M55 27.5C55 42.6878 42.6878 55 27.5 55C12.3122 55 0 42.6878 0 27.5C0 12.3122 12.3122 0 27.5 0C42.6878 0 55 12.3122 55 27.5Z"
const moonPath = "M12.5 25C12.5 40.1878 27.5 55 27.5 55C12.3122 55 0 42.6878 0 27.5C0 12.3122 12.3122 0 27.5 0C27.5 0 12.5 9.81217 12.5 25Z" 

const svg = document.querySelector('.modesvg')

// preloading animation
window.addEventListener('load', () => {
    const preloader = document.querySelector('.preloader')
    preloader.classList.add('preloader-finish')
})

// dark mode implementation

let toggle = false
// if (localStorage.getItem("dark") === null || localStorage.getItem("dark") == 'False') {
//     toggle = false
// }
// else{
//     toggle = true
// }

svg.addEventListener('click',(e) => {
    e.preventDefault()
    const timeline = anime.timeline({
        duration: 750,
        easing: "easeOutExpo"
    })
    timeline.add({
        targets: ".sun",
        d: [{value: toggle ? sunPath : moonPath}]
    })
    .add({
        targets: ".modesvg",
        rotate: 320
    },"-=350")
    .add({
        targets: ".home",
        backgroundColor: toggle ? "rgb(255,255,255)" : "rgb(22,22,22)"
    },"-=700")
    .add({
        targets: [".mode", "body", ".content-data", "header"],
        color: toggle ? "rgb(22,22,22)" : "rgb(255,255,255)",
        backgroundColor: toggle ? "rgb(255,255,255)" : "rgb(22,22,22)"
    },"-=700")
    .add({
        targets: [".g2"],
        color: toggle ? "rgb(255,255,255)" : "rgb(22,22,22)",
        backgroundColor: toggle ? "rgb(255,255,255)" : "rgb(22,22,22)"
    },"-=700")
    if(!toggle){
        toggle = true
        //localStorage.setItem('dark', 'True')
    }
    else{
        toggle = false
        //localStorage.setItem('dark', 'False')
    }
})
