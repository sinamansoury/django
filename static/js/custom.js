function sendRentComment(rentId, subId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    $.get('/rent/add-comment', {
        rent_comment: comment,
        rent_id: rentId,
        parent_id: parentId,
    }).then(res => {
        $('#reviews').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');
            if(parentId !== null && parentId !== ''){
            document.getElementById('single_'+ parentId).scrollIntoView({behavior:"smooth"})
        }else{
            document.getElementById('reviews').scrollIntoView({behavior:"smooth"})
        }

    });
}
function fillAnswer(parentId){
    $('#parent_id').val(parentId)
    document.getElementById('comment_form').scrollIntoView({behavior:"smooth"})
}

function sendProductComment(productId, subId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    $.get('/product-list/add-comment', {
        product_comment: comment,
        product_id: productId,
        parent_id: parentId,
    }).then(res => {
        $('#reviews').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');
        if(parentId !== null && parentId !== ''){
            document.getElementById('single_'+ parentId).scrollIntoView({behavior:"smooth"})
        }else{
            document.getElementById('reviews').scrollIntoView({behavior:"smooth"})
        }
    });
}
function removeProduct(detailId) {
                $.get('/dashboard/delete-product?detail_id=' + detailId
                ).then(res => {
                    if (res.status === 'success'){
                        $('#order-detail').html(res.data)
                    }
                })
            }
function changeProductNumber(detailId, stateId) {
    $.get('/dashboard/change-product-number?detail_id=' + detailId +"&state=" + stateId
    ).then(res => {
        if (res.status === 'success'){
            $('#order-detail').html(res.data)
        }
        if (res.status === 'error_product_number'){
            Swal.fire({
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "#428bca",
            confirmButtonText: res.confirmButtonText,
        })
        }
    })
}

function removeRentProduct(detailId) {
                $.get('/dashboard/delete-rent-product?detail_id=' + detailId
                ).then(res => {
                    if (res.status === 'success'){
                        $('#order-detail').html(res.data)
                    }
                })
            }
function changeRentProductNumber(detailId, stateId) {
    $.get('/dashboard/change-rent-product-number?detail_id=' + detailId +"&state=" + stateId
    ).then(res => {
        if (res.status === 'success'){
            $('#order-detail').html(res.data)
        }
        if (res.status === 'error_product_number'){
            Swal.fire({
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "#428bca",
            confirmButtonText: res.confirmButtonText,
        })
        }
    })
}

