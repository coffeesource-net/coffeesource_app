$(function () {
    'use strict'; 

    // Posts search by title.
    $('#id_title_search_field').on('input', function() {
      var search_text = $(this).val().toLowerCase();

      $('.CSEntriesList tr').each(function(i, obj) {
        var title = $(obj).data('entry-title').toLowerCase();

        if (!title.includes(search_text)) {
          $(obj).hide();
        } else {
          $(obj).show();
        }
      });
    });

    // Filter list by tag - Form submit.
    $('.backlink_filter_form form').on('submit', function() {
      var tag = $('#id_tag_filter_field').val();
      var data_tag = 'tag_' + tag;
      var tag_element = '<li data-tag="' + data_tag + '"><span class="badge badge-primary">' + tag + '</span> <a href="javascript:void(0)" class="fa fa-times tag_remove" aria-hidden="true"></a></li>';
      $('.applied_tag_filters').append(tag_element);

      $('.CSEntriesList tr').not("." + data_tag).hide();
      $('#id_tag_filter_field').val('');

      return false;
    });

    // Remove tag filter.
    $('.applied_tag_filters').on('click', '.tag_remove', function () {
      var tag_to_remove = $(this).closest('li').data('tag');

      var search_text = $('#id_title_search_field').val().toLowerCase();

      $('.CSEntriesList tr').each(function(i, obj) {

        // Check if there is any title filter appliced.
        var title = $(obj).data('entry-title').toLowerCase();
        if (!$(obj).hasClass(tag_to_remove)) {
          $(obj).show();

          if (search_text) {
            if (!title.includes(search_text)) {
              $(obj).hide();              
            }
          }
        }
      });

      $(this).parent().remove();
    });
});
