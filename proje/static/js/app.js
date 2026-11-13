var message = document.getElementById("message") //HTML'den mesajı çeker.

setTimeout(()=>{
    message.style.display = "none";

},4000) //4 saniye sonra mesajı kapat.(4000ms=4saniye)

//progress-bar class'larını çeker
//HTML'deki veriyi al yüzde olarak yazdır. JS görsel olarak gösterir.
document.querySelectorAll('.progress-bar').forEach(el => {
    el.style.width = el.dataset.width + '%';
});