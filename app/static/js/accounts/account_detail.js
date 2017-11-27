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
          }
          $('.CSAccountLoadPostsSpinner').hide();
      },
  });
}

$(function () {
    'use strict'; 

    $(document.body).on('touchmove', onScroll);
    $(window).on('scroll', onScroll);

    function onScroll(){
       if($(window).scrollTop() + $(window).height() == $(document).height()) {
          $('.CSAccountLoadPostsSpinner').show();
          bindScroll();
       }
    }
});
