var n = document.getElementsByClassName('update-cart')

for(i=0; i<n.length; i++){
    n[i].addEventListener('click', function(){
        var pname = this.dataset.product
        var action = this.dataset.action
        console.log('product name:', pname,'action:',action)
    })

}