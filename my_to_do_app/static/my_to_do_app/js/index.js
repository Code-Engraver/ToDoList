// https://docs.djangoproject.com/en/3.0/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function get_id(full_id) {
    return full_id.split('_').pop();
}

function validateForm() {
    let input_el = jQuery("#write_your_todo")
    let todo = input_el.val();
    if (todo.length <= 0 || todo.length > 100) {
        jQuery("#invalidate").removeClass("d-none");

        input_el.val("");
        input_el.focus();
        return false;
    }
    return true;
}

function validateUpdateForm(pk) {
    let input_el = jQuery(`#edit_your_todo_${pk}`);
    let todo = input_el.val();
    if (todo.length <= 0 || todo.length > 100) {
        jQuery(`#invalidateUpdate_${pk}`).removeClass("d-none");

        input_el.val("");
        input_el.focus();
        return false;
    }
    return true;
}

jQuery(document).ready(function() {
    let write_your_todo = jQuery("#write_your_todo")
    let progress = jQuery("#progress")

    write_your_todo.keydown(function() {
        jQuery("#invalidate").addClass("d-none");
    });

    write_your_todo.keyup(function() {
        let text = jQuery(this).val();
        let text_length = text.length
        if (text_length > 100) {
            jQuery("#invalidate").removeClass("d-none");
            write_your_todo.val(text.slice(0, 100));
            return;
        }
        progress.css("width", text_length + "%");
        progress.html(text_length + "/100");
    });

    jQuery("[id^=done]").click(function(){
        let form = jQuery(`
            <form action="/doneTodo/" method="post">
                <input type="hidden" value="${csrftoken}" name="csrfmiddlewaretoken">
                <input type="hidden" value=${get_id(jQuery(this).attr("id"))} name="id"/>
            </form>
        `)
        jQuery('body').append(form);
        form.submit();
    });

    jQuery("[id^=delete]").click(function(){
        if (!confirm("Delete it?")) {
            return
        }
        let form = jQuery(`
            <form action="/deleteTodo/" method="post">
                <input type="hidden" value="${csrftoken}" name="csrfmiddlewaretoken">
                <input type="hidden" value=${get_id(jQuery(this).attr("id"))} name="id"/>
            </form>
        `)
        jQuery('body').append(form);
        form.submit();
    });

    jQuery("[id^=edit_your_todo]").keydown(function() {
        jQuery(`#invalidateUpdate_${get_id(jQuery(this).attr("id"))}`).addClass("d-none");
    });
});
