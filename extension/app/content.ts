import * as $ from 'jquery';
import 'arrive'

function hasComments(): Boolean {
    return $('.comment-area').length > 0;
}

function addMagicButton(): void {
    $('.author-comment[data-uid="-1"]').each((_, element) => {
        $(element)
            .prev()
            .filter((_, el) => $(el).find('input').length === 0)
            .append($('<input data-magic type="button" value="施法">'))
    });
}

if (hasComments()) {
    const body: any = document.body;
    body.arrive('.item-comment', { existing: true, onceOnly: true }, () => {
        addMagicButton();
    });
    $('.comment-area').delegate('input[data-magic]', 'click', function () {
        const id = $(this).closest('.item-comment').attr('id').replace(/c-/i, '');
        $(this).val('施法中...')
        $.ajax({
            method: 'get',
            url: '//mcfun.trisolaries.com/comment',
            dataType: 'json',
            data: { id },
        })
            .then((res) => {
                if ($(this).closest('.content-comment').length > 0) {
                    $(this).closest('.content-comment').html(res.content);
                } else {
                    $(this).prev('.content-comment').html(res.content);
                }
                $(this).remove();
            })
            .catch(() => { $(this).val('施法失败') })
    });
}