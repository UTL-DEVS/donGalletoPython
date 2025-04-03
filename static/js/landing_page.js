$(function() {
  
    // SCROLL-TO ANIMATION
    $('a[href*="#"]:not([href="#"])').click(function() {
      if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        if (target.length) {
          $('html, body').animate({
            scrollTop: target.offset().top
          }, 1000);
          return false;
        }
      }
    });
    
    
   // FIXED NAV AFTER SCROLL
   document.onscroll = function() {
      if( $(window).scrollTop() > $('.cover').height() ) {
          $('nav.navbar').removeClass('sticky-top').addClass('fixed-top');
      }
  };
    
  });
  
  