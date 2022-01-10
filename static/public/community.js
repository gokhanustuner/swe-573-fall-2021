document.addEventListener("DOMContentLoaded", function() {
    let searchBar = document.getElementById('search-bar');
    let previousQueryLength;
    const monthNames = ["January", "February", "March", "April", "May", "June",
"July", "August", "September", "October", "November", "December"];
    searchBar.addEventListener('keyup', function(event) {
        event.preventDefault()
        let query = $('#search-bar').val();
        if (query.length >= 3 && previousQueryLength !== query.length) {
            let request = axios.get('/search/?search=' + query)
                .then(function (response) {
                    $('#search-wrapper .list-group-item').remove();
                    if (response.data.services_matching_by_title.length > 0) {
                        let newDiv3 = document.createElement('div')
                        let newLi1 = document.createElement('li');
                        $(newLi1).addClass('list-group-item d-flex justify-content-between align-items-start service-item');
                        $(newLi1).css('background-color', '#cccccc');
                        $(newDiv3).addClass('fw-100');
                        $(newDiv3).addClass('ms-2 me-auto');
                        $(newDiv3).html('Services matching with title');
                        $(newLi1).append(newDiv3);
                        $('#search-wrapper').append(newLi1);
                    }
                    for (let x = 0; x < response.data.services_matching_by_title.length; x++) {
                        let dateObj = new Date(response.data.services_matching_by_title[x].start_date);
                        let newLi = document.createElement('li');
                        let newDiv1 = document.createElement('div');
                        let newDiv2 = document.createElement('div');
                        let newSpan = document.createElement('span');

                        $(newLi).addClass('list-group-item d-flex justify-content-between align-items-start service-with-title-item');
                        $(newLi).attr('id', 'service_with_title-' + x);
                        $(newDiv1).addClass('ms-2 me-auto');
                        $(newLi).css('cursor', 'pointer');
                        $(newDiv2).addClass('fw-bold');
                        $(newDiv2).html(response.data.services_matching_by_title[x].title);
                        $(newSpan).addClass('badge bg-primary rounded-pill');
                        $(newDiv1).html(
                            newDiv2.outerHTML + response.data.services_matching_by_title[x].owner.full_name + ' ' + dateObj.toLocaleDateString() + ' ' + dateObj.toLocaleTimeString()
                        );
                        $(newLi).append(newDiv1);
                        $(newLi).append(newSpan);
                        $('#search-wrapper').css('display', 'flex');
                        $('#search-wrapper').append(newLi);
                    }

                    if (response.data.services_matching_by_owners_full_name.length > 0) {
                        let newDiv3 = document.createElement('div')
                        let newLi1 = document.createElement('li');
                        $(newLi1).addClass('list-group-item d-flex justify-content-between align-items-start');
                        $(newLi1).css('background-color', '#cccccc');
                        $(newDiv3).addClass('fw-100');
                        $(newDiv3).addClass('ms-2 me-auto');
                        $(newDiv3).html('Services matching with owner');
                        $(newLi1).append(newDiv3);
                        $('#search-wrapper').append(newLi1);
                    }
                    for (let x = 0; x < response.data.services_matching_by_owners_full_name.length; x++) {
                        let dateObj = new Date(response.data.services_matching_by_owners_full_name[x].start_date);
                        let newLi = document.createElement('li');
                        let newDiv1 = document.createElement('div');
                        let newDiv2 = document.createElement('div');
                        let newSpan = document.createElement('span');

                        $(newLi).addClass('list-group-item d-flex justify-content-between align-items-start service-with-owner-item');
                        $(newLi).attr('id', 'service_with_owner-' + x);
                        $(newDiv1).addClass('ms-2 me-auto');
                        $(newLi).css('cursor', 'pointer');
                        $(newDiv2).addClass('fw-bold');
                        $(newDiv2).html(response.data.services_matching_by_owners_full_name[x].title);
                        $(newSpan).addClass('badge bg-primary rounded-pill');
                        $(newDiv1).html(
                            newDiv2.outerHTML + response.data.services_matching_by_owners_full_name[x].owner.full_name + ' ' + dateObj.toLocaleDateString() + ' ' + dateObj.toLocaleTimeString()
                        );
                        $(newLi).append(newDiv1);
                        $(newLi).append(newSpan);
                        $('#search-wrapper').css('display', 'flex');
                        $('#search-wrapper').append(newLi);
                    }

                    if (response.data.events_matching_by_title.length > 0) {
                        let newDiv3 = document.createElement('div')
                        let newLi1 = document.createElement('li');
                        $(newLi1).addClass('list-group-item d-flex justify-content-between align-items-start');
                        $(newLi1).css('background-color', '#cccccc');
                        $(newDiv3).addClass('fw-100');
                        $(newDiv3).addClass('ms-2 me-auto');
                        $(newDiv3).html('Events matching with title');
                        $(newLi1).append(newDiv3);
                        $('#search-wrapper').append(newLi1);
                    }
                    for (let x = 0; x < response.data.events_matching_by_title.length; x++) {
                        let dateObj = new Date(response.data.events_matching_by_title[x].start_date);
                        let newLi = document.createElement('li');
                        let newDiv1 = document.createElement('div');
                        let newDiv2 = document.createElement('div');
                        let newSpan = document.createElement('span');

                        $(newLi).addClass('list-group-item d-flex justify-content-between align-items-start event-with-title-item');
                        $(newLi).attr('id', 'event_with_title-' + x);
                        $(newDiv1).addClass('ms-2 me-auto');
                        $(newLi).css('cursor', 'pointer');
                        $(newDiv2).addClass('fw-bold');
                        $(newDiv2).html(response.data.events_matching_by_title[x].title);
                        $(newSpan).addClass('badge bg-primary rounded-pill');
                        $(newDiv1).html(
                            newDiv2.outerHTML + response.data.events_matching_by_title[x].owner.full_name + ' ' + dateObj.toLocaleDateString() + ' ' + dateObj.toLocaleTimeString()
                        );
                        $(newLi).append(newDiv1);
                        $(newLi).append(newSpan);
                        $('#search-wrapper').css('display', 'flex');
                        $('#search-wrapper').append(newLi);
                    }

                    if (response.data.events_matching_by_owners_full_name.length > 0) {
                        let newDiv3 = document.createElement('div')
                        let newLi1 = document.createElement('li');
                        $(newLi1).addClass('list-group-item d-flex justify-content-between align-items-start');
                        $(newLi1).css('background-color', '#cccccc');
                        $(newDiv3).addClass('fw-100');
                        $(newDiv3).addClass('ms-2 me-auto');
                        $(newDiv3).html('Events matching with owner');
                        $(newLi1).append(newDiv3);
                        $('#search-wrapper').append(newLi1);
                    }
                    for (let x = 0; x < response.data.events_matching_by_owners_full_name.length; x++) {
                        let dateObj = new Date(response.data.events_matching_by_owners_full_name[x].start_date);
                        let newLi = document.createElement('li');
                        let newDiv1 = document.createElement('div');
                        let newDiv2 = document.createElement('div');
                        let newSpan = document.createElement('span');

                        $(newLi).addClass('list-group-item d-flex justify-content-between align-items-start event-with-owner-item');
                        $(newLi).attr('id', 'event_with_owner_id-' + x);
                        $(newDiv1).addClass('ms-2 me-auto');
                        $(newLi).css('cursor', 'pointer');
                        $(newDiv2).addClass('fw-bold');
                        $(newDiv2).html(response.data.events_matching_by_owners_full_name[x].title);
                        $(newSpan).addClass('badge bg-primary rounded-pill');
                        $(newDiv1).html(
                            newDiv2.outerHTML + response.data.events_matching_by_owners_full_name[x].owner.full_name + ' ' + dateObj.toLocaleDateString() + ' ' + dateObj.toLocaleTimeString()
                        );
                        $(newLi).append(newDiv1);
                        $(newLi).append(newSpan);
                        $('#search-wrapper').css('display', 'flex');
                        $('#search-wrapper').append(newLi);
                    }

                    $('.service-with-title-item').click(function() {
                        let resultIndex = $(this).attr('id').split('-')[1];
                        window.top.location.href = '/services/' + response.data.services_matching_by_title[resultIndex].uuid;
                    });
                    $('.service-with-owner-item').click(function() {
                        let resultIndex = $(this).attr('id').split('-')[1];
                        window.top.location.href = '/services/' + response.data.services_matching_by_owners_full_name[resultIndex].uuid;
                    });
                    $('.event-with-title-item').click(function() {
                        let resultIndex = $(this).attr('id').split('-')[1];
                        window.top.location.href = '/events/' + response.data.events_matching_by_title[resultIndex].uuid;
                    });
                    $('.event-with-owner-item').click(function() {
                        let resultIndex = $(this).attr('id').split('-')[1];
                        window.top.location.href = '/events/' + response.data.events_matching_by_owners_full_name[resultIndex].uuid;
                    });

                    request = null;
                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                }).then(function () {
                    previousQueryLength = query.length
                })
        }
    })

    $(document).mouseup(function(e) {
        let container = $('#search-wrapper');

        if (!container.is(e.target) && container.has(e.target).length === 0)
        {
            container.hide();
        }
    });
});