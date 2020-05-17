const usernameInput = document.querySelector('#anayzeFormUsernameInput');
const postsInput = document.querySelector('#analyzeFormNumberInput');
const getPostsButton = document.querySelector('#getPostsButton');
const loadingButton = document.querySelector('#loadingButton');
const moreInfoButton = document.querySelector('#more-info-button');
const moreInfoBox = document.querySelector('#more-info-box');
const homeButton = document.querySelector('home-button');
var onHome = true;


getPostsButton.addEventListener('click', () => {
  getPostsButton.style.display = 'none';
  loadingButton.style.display = 'block';

  usernameInput.setAttribute('readonly', 'true');
  postsInput.setAttribute('readonly', 'true');
  homeButton.classList.remove("active");
  onHome = false;
})



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


