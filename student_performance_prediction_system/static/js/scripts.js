// -------------------------
// MODAL CLOSE ON OUTSIDE CLICK
// -------------------------
window.onclick = function(event) {
    let modals = ['modal10','modalInter','modalDegree'];
    modals.forEach(function(m){
        let modal = document.getElementById(m);
        if(event.target == modal){ modal.style.display = "none"; }
    });
}

// -------------------------
// 3D HOVER EFFECT FOR CARDS
// -------------------------
let cards = document.querySelectorAll('.card');
cards.forEach(card => {
    card.addEventListener('mousemove', (e)=>{
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.transform = `rotateY(${(x - rect.width/2)/20}deg) rotateX(${-(y - rect.height/2)/20}deg) scale(1.03)`;
    });
    card.addEventListener('mouseleave', ()=>{
        card.style.transform='rotateY(0deg) rotateX(0deg) scale(1)';
    });
});

// -------------------------
// TOGGLE PASSWORD VISIBILITY
// -------------------------
function togglePassword() {
    let pass = document.getElementById("password");
    if(pass.type === "password"){ pass.type = "text"; }
    else{ pass.type = "password"; }
}

// -------------------------
// PDF DOWNLOAD FUNCTION
// -------------------------
function downloadPDF(studentName){
    const { jsPDF } = window.jspdf;
    let pdf = new jsPDF('p','mm','a4');
    pdf.text("Student Performance Report", 20, 20);
    
    // Collect student info cards dynamically
    let cards = document.querySelectorAll('.card');
    let yPos = 30;
    cards.forEach(c=>{
        let text = c.innerText.split('\n').join(' | ');
        pdf.text(text, 20, yPos);
        yPos += 10 + text.length/10;
        if(yPos > 280){ pdf.addPage(); yPos = 20; }
    });
    pdf.save(studentName + "_Report.pdf");
}

// -------------------------
// DASHBOARD CHARTS
// -------------------------

// Attendance chart (Bar)
const attendanceCanvas = document.getElementById('attendanceChart');
if(attendanceCanvas){
    new Chart(attendanceCanvas.getContext('2d'),{
        type:'bar',
        data:{
            labels: window.semesters || ["Sem1","Sem2","Sem3","Sem4","Sem5","Sem6"],
            datasets:[
                {label:'Semester Marks', data: window.sem_marks || [0,0,0,0,0,0], backgroundColor:'rgba(75,192,192,0.7)'},
                {label:'Semester %', data: window.sem_perc || [0,0,0,0,0,0], backgroundColor:'rgba(255,99,132,0.7)'}
            ]
        },
        options:{ responsive:true }
    });
}

// BCA mini line chart
const bcaCanvas = document.getElementById('bcaChart');
if(bcaCanvas){
    new Chart(bcaCanvas.getContext('2d'),{
        type:'line',
        data:{
            labels: window.bca_labels || ["Internal1","Internal2","Assignment","Lab","Mini","Major"],
            datasets:[{
                label:'BCA Scores',
                data: window.bca_scores || [0,0,0,0,0,0],
                backgroundColor:'rgba(10,133,140,0.4)',
                borderColor:'#0A858C',
                fill:true,
                tension:0.3
            }]
        },
        options:{ responsive:true }
    });
}

// -------------------------
// MINI GRAPHS / ADDITIONAL CHARTS
// -------------------------

// Skill Matrix Radar
const skillCanvas = document.getElementById('skillChart');
if(skillCanvas){
    new Chart(skillCanvas.getContext('2d'),{
        type:'radar',
        data:{
            labels: ["Communication","Programming","Logical","Leadership","Technical"],
            datasets:[{
                label:"Skill Level",
                data: [70,75,72,68,74], // dynamic values can be passed here
                backgroundColor:'rgba(255,99,132,0.2)',
                borderColor:'rgba(255,99,132,1)',
                pointBackgroundColor:'rgba(255,99,132,1)'
            }]
        },
        options:{ responsive:true }
    });
}

// Career Prediction Doughnut
const careerCanvas = document.getElementById('careerChart');
if(careerCanvas){
    new Chart(careerCanvas.getContext('2d'),{
        type:'doughnut',
        data:{
            labels: ["Placement","Higher Studies","Entrepreneurship"],
            datasets:[{
                data: [60,30,10],
                backgroundColor:['#0A858C','#FFD93D','#FF6B6B']
            }]
        },
        options:{ responsive:true }
    });
}

// Placement Readiness Doughnut
const placementCanvas = document.getElementById('placementChart');
if(placementCanvas){
    new Chart(placementCanvas.getContext('2d'),{
        type:'doughnut',
        data:{
            labels: ["Ready","Needs Improvement"],
            datasets:[{
                data: [6,4], // dynamic: ready, needs improvement
                backgroundColor:['#6BCB77','#FF6B6B']
            }]
        },
        options:{ responsive:true }
    });
}

// Line chart for manual prediction inputs
const inputCanvas = document.getElementById('inputChart');
if(inputCanvas){
    new Chart(inputCanvas.getContext('2d'),{
        type: 'bar',
        data: {
            labels: Object.keys(window.student_info || {}),
            datasets: [{
                label: 'Student Input Scores',
                data: Object.values(window.student_info || {}),
                backgroundColor: 'rgba(75,192,192,0.7)'
            }]
        },
        options: { responsive:true }
    });
}