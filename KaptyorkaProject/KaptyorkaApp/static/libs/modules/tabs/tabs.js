$(function () {
    $('.btn-scrollable').on('click', function () {
        btnId = $(this).attr('id');
        $('.btn-scrollable.active-tab-label').removeClass('active-tab-label').addClass('hidden-tab-label');
        $(this).addClass('active-tab-label').removeClass('hidden-tab-label').blur();
        var menuId = btnId.substring(4, btnId.length);
        $('[href="#' + menuId + '"]').tab('show');
        $('.tab-pane').removeClass('in').removeClass('active').removeClass('show');
        $('#' + menuId).addClass('in').addClass('active').addClass('show');
        $.fn.switchControlTabsButtons();
        updateData();
    });

    $('.next-step, .prev-step').on('click', function (e) {
        var $activeTab = $('.tab-pane.active');
        if ($(e.target).hasClass('next-step')) {
            var nextTabId = $activeTab.next('.tab-pane').attr('id');
            if (nextTabId != undefined) {
                var activeTabId = $activeTab.attr('id');

                var btn = $('#btn-' + activeTabId);
                $('#btn-' + activeTabId).removeClass('active-tab-label').addClass('hidden-tab-label');
                var btn2 = $('#btn-' + nextTabId);
                $('#btn-' + nextTabId).removeClass('hidden-tab-label').addClass('active-tab-label');
                $('#' + activeTabId).removeClass('in').removeClass('active').removeClass('show');
                $('#' + nextTabId).addClass('in').addClass('active').addClass('show');
            }
        }
        else {
            var prevTabId = $activeTab.prev('.tab-pane').attr('id');
            if (prevTabId != undefined) {
                var activeTabId = $activeTab.attr('id');
                var btn = $('#btn-' + activeTabId);
                $('#btn-' + activeTabId).removeClass('active-tab-label').addClass('hidden-tab-label');
                var btn2 = $('#btn-' + prevTabId);
                $('#btn-' + prevTabId).removeClass('hidden-tab-label').addClass('active-tab-label');
                // $('[href="#' + prevTabId + '"]').tab('show');
                $('#' + activeTabId).removeClass('in').removeClass('active').removeClass('show');
                $('#' + prevTabId).addClass('in').addClass('active').addClass('show');
            }

        }
        $.fn.switchControlTabsButtons();
        updateData();
    });

    $.fn.switchControlTabsButtons = function () {
        var $activeTab = $('.tab-pane.active');
        var nextTabId = $activeTab.next('.tab-pane').attr('id');
        if (nextTabId == undefined) {
            $('.next-step').hide();
            $('.last-step').show();
        }
        else {
            $('.next-step').show();
            $('.last-step').hide();
        }
        var prevTabId = $activeTab.prev('.tab-pane').attr('id');
        if (prevTabId == undefined) {
            $('.prev-step').prop('disabled', true);
        }
        else {
            $('.prev-step').prop('disabled', false);
        }
    }

});

function updateData() {
    // RESPONSIBLE PERSON
    $("#responsiblePersonCDataField")[0].innerText =  $(".filter-option-inner-inner")[0].innerText;
    if ($(".filter-option-inner-inner")[0].innerText == "Выберите контакт"){
        $("#responsiblePersonCDataField")[0].innerText = "Не выбрано";
        $("#responsiblePersonCDataField").addClass("required-alert");
    }
    else {
        $("#responsiblePersonCDataField").removeClass("required-alert");
    }
    // LEAD
    $("#leadCDataField")[0].innerText =  byId("leadInputField").value;
    if ($("#leadCDataField")[0].innerText == ""){
        $("#leadCDataField")[0].innerText = "Не выбрано";
        $("#leadCDataField").addClass("required-alert");
    }
    else {
        $("#leadCDataField").removeClass("required-alert");
    }
    // TYPE OF HIKE
    $("#typeOfHikeCDataField")[0].innerText =  byId("typeOfHikeSelector").value;
    // TIME 
    $("#datesOfRentCDataField")[0].innerText = beauty_date_interval(byId("start_day").value, byId("end_day").value);
    console.log(3);
}

function validateData(textIfValid, textIfNotValid) {

}

