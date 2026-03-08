console.log("AI Attendance Dashboard Loaded")

// simple loading animation for buttons
document.querySelectorAll(".card").forEach(card=>{
card.addEventListener("click",()=>{
card.style.opacity="0.6"
})
})