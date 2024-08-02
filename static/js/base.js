const searchon = document.querySelector('#searchopen');
const searchoff = document.querySelector('#removesearch');
const searchinput = document.querySelector('.seachinput');

searchinput.style.display = "none";

searchon.addEventListener('click',()=>{
    if (searchinput.style.display === 'none') {
        searchinput.style.display = 'flex';
    } else {
        searchinput.style.display = 'none';
    }
});

searchoff.addEventListener('click',()=>{
    if (searchinput.style.display === 'flex') {
        searchinput.style.display = 'none';
    } else {
        searchinput.style.display = 'flex';
    }
});

// darkmode

const darkmode =document.querySelector('#checkbox');
let body = document.body;
const logoImage = document.querySelector('logo img');
const logoImage2 = document.querySelector('.titleicon img');


const idDarkMode = localStorage.getItem('darkMode') === 'true';


if (idDarkMode) {
    body.classList.add('dark');
    darkmode.checked = true;
    logoImage.src = '/static/images/favicon.png/'
    logoImage2.src = '/static/images/favicon.png/'
} else {
    logoImage.src = '/static/images/logo.png/'
    logoImage2.src = '/static/images/chef.png/'

}

darkmode.addEventListener('change',()=>{
    if (darkmode.checked) {
        body.classList.add('dark')
        logoImage.src = '/static/images/favicon.png/'
        logoImage2.src = '/static/images/favicon.png/'
        localStorage.setItem('darkMode', 'true');
    } else {
        body.classList.remove('dark')
        logoImage.src = '/static/images/logo.png/'
        logoImage2.src = '/static/images/logo.png/'
        localStorage.setItem('darkMode', 'false');
    }
})