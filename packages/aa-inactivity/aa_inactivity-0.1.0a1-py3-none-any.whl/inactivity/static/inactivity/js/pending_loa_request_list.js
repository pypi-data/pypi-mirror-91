/* global loaSettings */

$(document).ready(function () {
    "use strict";

    var listPendingRequestsUrl = loaSettings.listPendingRequestsUrl;
    var csrfToken = loaSettings.csrfToken;
    function approveRequestUrl(id) {
        return loaSettings.approveRequestUrl.replace("12345",id);
    }
    function cancelRequestUrl(id) {
        return loaSettings.cancelRequestUrl.replace("12345",id);
    }
    var csrfToken = loaSettings.csrfToken;

    /* dataTable def */
    $("#table-requests").DataTable({
        ajax: {
            url: listPendingRequestsUrl,
            dataSrc: "",
            cache: false,
        },

        columns: [
            { data: "user" },
            { data: "start" },
            { data: "end" },
            { data: "pk" },
        ],

        lengthMenu: [
            [10, 25, 50, 100, -1],
            [10, 25, 50, 100, "All"],
        ],


        columnDefs: [
            { sortable: false, targets: [3] },
            {
                render: function (data, type, row) {
                    if (type === "display") {
                        return (
                            '<form method="post" class="inline" action="' + cancelRequestUrl(data) + '">' +
                        csrfToken +
                            '<button type="submit" class="btn btn-sm btn-danger btn-square">' +
                            '<span class="fas fa-trash-alt"></span>' +
                            '</button></form>' +
                            '<form method="post" class="inline" action="' + approveRequestUrl(data) + '">' +
                        csrfToken +
                            '<button type="submit" class="btn btn-sm btn-primary btn-square">' +
                            '<span class="fas fa-check"></span>' +
                            '</button></form>'
                        );
                    }

                    return data;
                },
                targets: [3],
            },
        ],

        order: [
            [0, "desc"],
        ],
    });
});
