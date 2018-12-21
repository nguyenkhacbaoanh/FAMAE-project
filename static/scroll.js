$(document).ready(function() {
	
    var headerHeight = $('ul').outerHeight(); // Target your header navigation here
      
    $('li').click(function(e) {
        
        var targetHref = $(this).attr('href');
        
      $('html, body').animate({
          scrollTop: $(targetHref).offset().top - headerHeight // Add it to the calculation here
      }, 700);
      
      e.preventDefault();
    });
  });

  $(function() {
    var header = $(".cc");
    header.addClass("scrolled");
  
    $(window).scroll(function() {    
        var scroll = $(window).scrollTop();
        if (scroll >= 0 && scroll <= 100) {
            header.addClass("scrolled");
        } else {
            header.removeClass("scrolled");
        }
    });
});