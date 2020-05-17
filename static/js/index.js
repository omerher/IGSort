const usernameInput = document.querySelector('#anayzeFormUsernameInput');
const postsInput = document.querySelector('#analyzeFormNumberInput');
const getPostsButton = document.querySelector('#getPostsButton');
const loadingButton = document.querySelector('#loadingButton');


getPostsButton.addEventListener('click', () => {
  getPostsButton.style.display = 'none';
  loadingButton.style.display = 'block';

  usernameInput.setAttribute('readonly', 'true');
  postsInput.setAttribute('readonly', 'true');
})
