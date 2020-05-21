var $grid = $('.grid');
$grid.imagesLoaded(function(){
  $grid.masonry({
  columnWidth: '.grid-sizer',
  itemSelector: '.grid-item',
  horizontalOrder: true,
  gutter: 20,
  transitionDuration: '0.2s',
  initLayout: false
  });
});

$grid.masonry();

filterSelection("all")

function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("filterDiv");
  if (c == "all") c = "";
  // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
  for (i = 0; i < x.length; i++) {
    removeClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) addClass(x[i], "show");
  }
}

// Show filtered elements
function addClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {
      element.className += " " + arr2[i];
    }
  }
}

// Hide elements that are not selected
function removeClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}

// // Add active class to the current control button (highlight it)
// var btnContainer = document.getElementById("filterButtons");
// var btns = btnContainer.getElementsByClassName("btn");
// for (var i = 0; i < btns.length; i++) {
//   btns[i].addEventListener("click", function() {
//     var current = document.querySelector(".btn-primary");
//     current.classList.toggle("btn-primary")
//     current.classList.toggle("btn-secondary")
//     this.classList.toggle("btn-primary")
//     this.classList.toggle("btn-secondary")
//   });
// }

var captions = document.querySelectorAll(".caption-overflow");
for (i = 0; i < captions.length; i++) {
  captions[i].addEventListener('click', function () {
    this.classList.toggle('caption-overflow')
  })
}