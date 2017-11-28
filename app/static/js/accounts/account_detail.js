function bindScroll(){
  var last_loaded_id = $( ".CSEntriesList >li:last-child" ).data('entry-id');
  var load_account_posts_url = $('.CSEntriesList').data('ax-load-account-posts-url') + '&last_entry_id=' + last_loaded_id;

  $.ajax({
      url : load_account_posts_url,
      type: "GET",
      processData: false,
      contentType: false,
      success:function(response){
          if (response.action === 'load') {
              $('.CSEntriesList').append(response.content);
          } else {
            $('.CSLoadPostsButtom').hide();            
          }
          $('.CSAccountLoadPostsSpinner').hide();
          $('.CSLoadPostsButtom').addClass('enabledLoad'); 
      },
  });
}

$(function () {
    'use strict'; 

    $('.CSLoadPostsButtom').on('click', function () {
        if ($(this).hasClass('enabledLoad')) {
          $('.CSAccountLoadPostsSpinner').show();
          $(this).removeClass('enabledLoad');
          bindScroll();
        }

        return false;
    });
});
