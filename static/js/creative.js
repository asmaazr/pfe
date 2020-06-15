(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });

})(jQuery); // End of use strict
//Annotated code
var text = $(".switcher").attr("shift").replace(/\ /g, '•').toUpperCase().split(','); //Get words, sort out spaces, put to uppercase and make an array.
var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789•".toUpperCase(); //allowed characters, case unspecific as it converts everything into uppercase.

var select = 0; //Which text is selected first
var length = Math.max.apply(Math, $.map(text, function (el) { return el.length })); //Length of longest string
var correct = 0; //Counter to see if all letters match
var selecttext = []; //Current held correct text
var fulltext = []; //Current held text, not always correct
var actualtext = ""; //Text displayed inside .switcher .display
var latch = true; //Just a fail safe to not skip a word

setInterval(flicker,40); //This is how fast the characters switch

write();
function write() {
  loadtext();
  for (var i = 0; i <length; i++) { //initiate fulltext with completely blank string
    fulltext[i] = "•";
  }
}

function loadtext() { //Fill selecttext with word and empty space padding •
  for (var i = 0; i <length; i++) {
    selecttext[i] = text[select][i];
    if (i >= text[select].length) {
      selecttext[i] = "•";
    }
  }
  latch = true; //open to check if words match
}
function flicker() { //Matching characters
  for (var i = 0; i < length; i++) { //cycle through letters
    if (selecttext[i] != fulltext[i]) { //does the varying character not match with the correct one
      if (fulltext[i] == "•") { //If it is at the end of the loop
        fulltext[i] = "A"; //Put to the beginning
      } else {
        fulltext[i] = chars[chars.indexOf(fulltext[i]) + 1]; //Increase character by 1
      }
      correct++; //means that the loop will not end this time around  
    }
  }
  for (var i = 0; i < length; i++) { //Stitch characters into a word
    actualtext += fulltext[i]; 
  }
  if (latch) {
    $(".switcher").text(actualtext); //Display the word
  }
  actualtext = ""; //and blanket
  if (correct == 0 && latch) { //If there are no errors and it can latch
    latch = false; //can't latch
    if (select >= text.length-1) { //increment word by 1 or loop
      select = 0;
    } else {
      select++;
    }
    setTimeout(loadtext,1500); //start next word after a pause, this is where latch comes into play
  }
  correct = 0; //reset correct after it is used
}




var SignupButtons = {
  request: function(element) { 
    element.classList.add('-request');
  },

  success: function(element) { 
    element.classList.remove('-request');
    element.classList.add('-success');
  },

  reset: function(element) { 
    element.classList.remove('-success');
  },
  
  flow: function(element) { 
    SignupButtons.request(element);

    setTimeout(function() { 
      SignupButtons.success(element);
    }, 2150);

    setTimeout(function() { 
      SignupButtons.reset(element);
    }, 4000);
  },

  init: function() {
    var buttons = document.querySelectorAll('button');

    for (let i = 0; i < buttons.length; i++) {
      var button = buttons[i];
      
      button.addEventListener('click', function() { 
        SignupButtons.flow(button);
      });
    }
  }
};




$('.counter').counterUp({
  delay: 100,
  time: 7000
});
$('.counter').addClass('animated fadeInDownBig');
$('h3').addClass('animated fadeIn');



new Awesomplete('input[data-multiple]', {
	filter: function(text, input) {
		return Awesomplete.FILTER_CONTAINS(text, input.match(/[^,]*$/)[0]);
	},

	item: function(text, input) {
		return Awesomplete.ITEM(text, input.match(/[^,]*$/)[0]);
	},

	replace: function(text) {
		var before = this.input.value.match(/^.+,\s*|/)[0];
		this.input.value = before + text + ", ";
	}
});