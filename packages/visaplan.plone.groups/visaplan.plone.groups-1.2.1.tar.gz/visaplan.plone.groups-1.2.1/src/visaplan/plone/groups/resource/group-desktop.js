function showelement(button) {
	var btn = $(button).attr('id');
	sellist = btn.split("_")[0];
	action = btn.split("_")[1];
	url = $('#'+sellist+' :selected').val().split("?");
	window.location.href = url[0]+'/'+action+'?'+url[1];
}
$(document).ready(function () {
	$('#collab ').chosen().change(function () {
		url = $('#collab :selected').val();
		if (url) {
		   $('#collab_view').removeProp('disabled');
		   $('#collab_structure-edit').removeProp('disabled');
		   $('#collab_view').removeClass('disabled');
		   $('#collab_structure-edit').removeClass('disabled');
		   $('#collab_view').addClass('btn-primary');
		   $('#collab_structure-edit').addClass('btn-primary');
		} else {
		   $('#collab_view').prop('disabled', 'disabled');
		   $('#collab_structure-edit').prop('disabled', 'disabled');
		   $('#collab_view').removeClass('btn-primary');
		   $('#collab_structure-edit').removeClass('btn-primary');
		}
	})
	$('#watched').chosen().change(function () {
		url = $('#watched :selected').val();
		if (url) {
		   $('#watched_view').removeProp('disabled');
		   $('#watched_view').removeClass('disabled');
		   $('#watched_view').addClass('btn-primary');
		} else {
		   $('#watched_view').prop('disabled', 'disabled');
		   $('#watched_view').addClass('disabled');
		   $('#watched_view').removeClass('btn-primary');
		}
	})
	$('div.list-action div.box p.link').show();
	function toggle_checked() {
		var checked = $(this).is(':checked'),
	        par = $(this).closest('div.list-action'),
			lab = $(this).closest('label');
		if (checked) {
			par.find('.empty').show();
			lab.attr('title', $(lab).data('checked'));
		} else {
			par.find('.empty').hide();
			lab.attr('title', $(lab).data('unchecked'));
		}
		if (console && console.log) {
			console.log('toggle_checked: '+checked);
		}
	}
	$('div.list-action div.box p.link input').each(toggle_checked);
	$('div.list-action div.box p.link input').change(toggle_checked);
});
