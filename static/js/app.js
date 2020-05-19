$(function(){
  var current = location.pathname;
  $('.nav-link').each(function(){
      var $this = $(this);
      // if the current path is like this link, make it active
      if($this.attr('href').indexOf(current) !== -1){
        if(current === "/"){
          $('#navHomeBtn').addClass('active')
        }else{
          $this.addClass('active');
        }  
      }
  })
})