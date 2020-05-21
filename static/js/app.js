function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

var offset = new Date().getTimezoneOffset();
setCookie('localTimeZoneOffset', offset, 14)

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