function LoadPostImages(){
  var last_loaded_id = $(".ImagesLinkList tr:last").data('entry-id');

  var load_account_posts_url = $('.ImagesLinkList').data('ax-load-posts-images-url') + '&last_entry_id=' + last_loaded_id;

  $.ajax({
      url : load_account_posts_url,
      type: "GET",
      processData: false,
      contentType: false,
      success:function(response){
          if (response.action === 'load') {
              $('.ImagesLinkList').append(response.content);
          } else {
            $('.LoadPostsImages').hide();            
          }
          $('.CSAccountLoadPostsSpinner').hide();
          $('.LoadPostsImages').addClass('enabledLoad'); 
      },
  });
}

$(function () {
    'use strict'; 

    $('.LoadPostsImages').on('click', function () {
        if ($(this).hasClass('enabledLoad')) {
          $('.CSAccountLoadPostsSpinner').show();
          $(this).removeClass('enabledLoad');
          LoadPostImages();
        }

        return false;
    });
});
