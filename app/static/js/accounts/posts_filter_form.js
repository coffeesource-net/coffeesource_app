function applyFilter() {
  var applied_tags_list = [];


  $('.applied_tag_filters li').each(function(i, obj) {
    applied_tags_list.push($(obj).data('tag'));
  });

  $('.CSEntriesList tr').each(function(i, obj) {
    var show_element_by_tag = false;

    for (var index in applied_tags_list) {
      var tag = applied_tags_list[index];

      if (!$(obj).hasClass(tag)) {
        show_element_by_tag = true;
      }
    }

    if (!show_element_by_tag) {
     $(obj).removeClass('hidden');
    } else {
      $(obj).addClass('hidden');
    }

    // Check if there is any applied filter by title.
    var show_element_by_tite = false;

    var title = $(obj).data('entry-title').toLowerCase();
    var search_title_key = $('#id_title_search_field').val().toLowerCase();

    if (search_title_key) {
      if (!title.includes(search_title_key)) {
        $(obj).addClass('hidden');
      } else if (title.includes(search_title_key) & !$(obj).hasClass('hidden')) {
        $(obj).removeClass('hidden');
      }
    }
  });
}

$(function () {
    'use strict'; 

    // Posts search by title.
    $('#id_title_search_field').on('input', function() {
      applyFilter();
    });

    // Filter list by tag - Form submit.
    $('.backlink_filter_form form').on('submit', function() {
      var tag = $('#id_tag_filter_field').val();
      var data_tag = 'tag_' + tag;

      var tag_element = '<li data-tag="' + data_tag + '"><span class="badge badge-primary">' + tag + '</span> <a href="javascript:void(0)" class="fa fa-times tag_remove" aria-hidden="true"></a></li>';

      // Check if filter tag has been previously added.
      var previously_added = false;
      $('.applied_tag_filters li').each(function(i, obj) {
        if ($(obj).data('tag') === data_tag) {
          previously_added = true;
        }
      });

      if (!previously_added) {
        $('.applied_tag_filters').append(tag_element);

        applyFilter();
      }
      $('#id_tag_filter_field').val('');

      return false;
    });

    // Remove tag filter.
    $('.applied_tag_filters').on('click', '.tag_remove', function () {
      var tag_to_remove = $(this).closest('li').data('tag');

      var search_text = $('#id_title_search_field').val().toLowerCase();
      $(this).parent().remove();

      applyFilter();
    });
});
