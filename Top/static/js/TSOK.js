jQuery('base.html').ready(function(){
  $('.dropdown-toggle').click(function(){
    $('.dropdown-toggle').css({
      'outline': 'none',
      'border-color': 'none !important'
    });
  });
  $('.register form input').after('<br>');
  $('.register form input[type=text]').attr('placeholder', "Имя пользователя");
  $('.register form input[name=password1]').attr('placeholder', "Пароль");
  $('.register form input[name=password2]').attr('placeholder', "Потвердить пароль");

  $('.login form input[type=text]').attr('placeholder', "Имя пользователя");
  $('.login form input[type=password]').attr('placeholder', "Пароль");
});
 
new Vue ({
  el: '.poisck_input',
  data: {
    poisck_text: ''
  },
});