function LoadPosts(){
  var last_loaded_id = $(".CSEntriesList tr:last").data('entry-id');
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

          // Check applied tags to filter
          var tags_list = []
          $('.applied_tag_filters li').each(function(i, obj) {
            tags_list.push($(obj).data('tag'));
          });

          // Check applied title search
          var search_text = $('#id_title_search_field').val().toLowerCase();

          $('.CSEntriesList tr').each(function(i, obj) {
            var hide_by_tag = false;

            for (var tag_idx in tags_list) {
              if ($(obj).hasClass(tags_list[tag_idx]) == false) {
                hide_by_tag = true
              }
            }

            if (hide_by_tag == true) {
              $(obj).hide();
            }

            var title = $(obj).data('entry-title').toLowerCase();

            if (search_text) {
              if (!title.includes(search_text)) {
                $(obj).hide();
              }
            }
          });
      },
  });
}

$(function () {
    'use strict'; 

    $('.CSLoadPostsButtom').on('click', function () {
        if ($(this).hasClass('enabledLoad')) {
          $('.CSAccountLoadPostsSpinner').show();
          $(this).removeClass('enabledLoad');
          LoadPosts();
        }

        return false;
    });
});
