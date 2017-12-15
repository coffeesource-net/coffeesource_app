function bindScroll(){
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

          var tags_list = []

          $('.applied_tag_filters li').each(function(i, obj) {
            tags_list.push($(obj).data('tag'));
          });

          $('.CSEntriesList tr').each(function(i, obj) {
            var hide = false;

            for (var tag_idx in tags_list) {
              if ($(obj).hasClass(tags_list[tag_idx]) == false) {
                hide = true
              }
            }

            if (hide == true) {
              $(obj).hide();
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
          bindScroll();
        }

        return false;
    });

    $('.backlink_filter_form form').on('submit', function() {
      var tag = $('#id_tag_filter_field').val();
      var data_tag = 'tag_' + tag;
      var tag_element = '<li data-tag="' + data_tag + '"><span class="badge badge-primary">' + tag + '</span> <a href="javascript:void(0)" class="fa fa-times tag_remove" aria-hidden="true"></a></li>';
      $('.applied_tag_filters').append(tag_element);

      $('.CSEntriesList tr').not("." + data_tag).hide();
      $('#id_tag_filter_field').val('');

      return false;
    });

    $('.applied_tag_filters').on('click', '.tag_remove', function () {
      var tag_to_remove = $(this).closest('li').data('tag');

      $('.CSEntriesList tr').not("." + tag_to_remove).show();
      $(this).parent().remove();
    });
});
