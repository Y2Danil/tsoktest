jQuery('base.html').ready(function(){
  $('.dropdown-toggle').click(function(){
    $('.dropdown-toggle').css({
      'outline': 'none',
      'border-color': 'none !important'
    });
  });
});
 
new Vue ({
  el: '.poisck_input',
  data: {
    poisck_text: ''
  },
});