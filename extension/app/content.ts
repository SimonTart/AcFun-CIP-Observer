import * as $ from 'jquery';
import 'arrive'

function isArticle(): Boolean {
  return $('#area-title-view').length > 0;
}

function addMagicButton():void {
  $('.author-comment[data-uid="-1"]:not(input)').each((_, element) => {
    $(element).prev().append($('<input data-magic type="button" value="施法">'))
  });
}

if (isArticle()) {
  const body:any = document.body;
  body.arrive('.area-pager',{ onceOnly: true, existing: true}, () => {
    addMagicButton();
  });
  $('#area-bottom-view').delegate('input[data-magic]', 'click', function() {
    const id = $(this).closest('.item-comment').attr('id').replace(/c-/i, '');
    $(this).val('施法中...')
    $.ajax({
      method: 'get',
      // url: '//acfun.trisolaries.com/comment',
      url: '//127.0.0.1:8000/comment',
      dataType: 'json',
      data: { id },
    })
    .then((res) => { $(this).closest('.content-comment').html(res.content) })
    .catch(() => { $(this).val('施法失败') })
  });
}