"use strict";
(() => {
 const menu = document.querySelector(".menu-toggle");
 const nav = document.getElementById("site-nav");
 if (menu && nav) {
  menu.addEventListener("click", () => { const open = menu.getAttribute("aria-expanded") !== "true"; menu.setAttribute("aria-expanded", String(open));menu.setAttribute("aria-label",open?"Close navigation":"Open navigation");nav.classList.toggle("open",open);});
  nav.addEventListener("click", e => {if(e.target.closest("a")){nav.classList.remove("open");menu.setAttribute("aria-expanded","false");menu.setAttribute("aria-label","Open navigation");}});
  document.addEventListener("keydown", e => {if(e.key==="Escape" && nav.classList.contains("open")){nav.classList.remove("open");menu.setAttribute("aria-expanded","false");menu.focus();}});
 }
 const year = document.getElementById("year");if(year)year.textContent=String(new Date().getFullYear());
 const buttons = Array.from(document.querySelectorAll(".filter-button"));
 const gallery = Array.from(document.querySelectorAll(".gallery-item"));
 const qs = new URLSearchParams(location.search);
 function filterTo(key){
  if(!["all","apparel","jigs","sample"].includes(key)) key="all";
  buttons.forEach(b => {const yes=b.dataset.filter===key;b.classList.toggle("active",yes);b.setAttribute("aria-pressed",String(yes));});
  gallery.forEach(g => {g.hidden=key!=="all" && g.dataset.category!==key;g.style.display=g.hidden?"none":"";});
 }
 buttons.forEach(b => b.addEventListener("click",()=>filterTo(b.dataset.filter)));
 if(buttons.length) filterTo(qs.get("category")||"all");
 const dialog=document.getElementById("photo-dialog");
 if(dialog && "showModal" in dialog){
  const img=document.getElementById("dialog-img"), caption=document.getElementById("dialog-caption"), close=dialog.querySelector(".dialog-close");
  gallery.forEach(card => card.addEventListener("click", () => {img.src=card.dataset.image;img.alt=card.querySelector("img")?.alt||card.dataset.caption;caption.textContent=card.dataset.caption;dialog.showModal();close.focus();}));
  close.addEventListener("click",()=>dialog.close());
  dialog.addEventListener("click",e=>{if(e.target===dialog)dialog.close();});
  dialog.addEventListener("close",()=>{img.removeAttribute("src");});
 }
 const form=document.getElementById("contact-form");
 if(form){
  const interest=qs.get("interest");if(interest && ["Apparel","Jigs"].includes(interest))form.elements.interest.value=interest;
  const status=document.getElementById("form-status");
  // Add Robert's verified Formspree endpoint; do not publish a fake email or endpoint.
  const FORM_ENDPOINT = "";
  form.addEventListener("submit", async event => {
   event.preventDefault();status.textContent="";status.className="form-status";
   if(!form.checkValidity()){form.reportValidity();return;}
   if(form.elements._gotcha.value)return;
   if(!/^https:\/\/formspree\.io\/f\/[a-zA-Z0-9]+$/.test(FORM_ENDPOINT)){
    status.classList.add("error");status.textContent="This demo form is not connected yet. Please ask the site owner to configure a verified contact endpoint. Your message has not been sent.";return;
   }
   const button=document.getElementById("submit-button");button.disabled=true;button.textContent="Sending…";
   try{
    const response=await fetch(FORM_ENDPOINT,{method:"POST",body:new FormData(form),headers:{"Accept":"application/json"}});
    if(!response.ok)throw new Error("Delivery failed");
    form.reset();status.classList.add("success");status.textContent="Your message was sent. Thank you for contacting Robert.";
   }catch(e){status.classList.add("error");status.textContent="Your message could not be delivered. Please try again later.";}
   finally{button.disabled=false;button.innerHTML="Submit inquiry <span aria-hidden=\"true\">↗</span>";}
  });
 }
})();
