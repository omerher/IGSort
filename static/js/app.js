const moreInfoButton = document.querySelector('#more-info-button');
const moreInfoBox = document.querySelector('#more-info-box');
const homeButton = document.querySelector('home-button');
var onHome = true;

moreInfoButton.addEventListener('click', () => {
  if(onHome){
      moreInfoBox.style.background = 'rgba(217, 30, 24, 0.15)';
      setTimeout(() => {moreInfoBox.style.background = 'none'} , 1500);
  }
  else{
    window.location.replace("{{ url_for('index') }}");
    onHome = true;
  }
  
})

homeButton.addEventListener('click', homeButton.classList.add("active"));