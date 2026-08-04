/* DeskRec website — shared UI behaviour */
(function () {
  "use strict";

  // Mobile burger menu
  var burger = document.querySelector(".burger");
  var menu = document.querySelector(".mobile-menu");
  if (burger && menu) {
    burger.addEventListener("click", function () {
      menu.classList.toggle("show");
      burger.setAttribute("aria-expanded", menu.classList.contains("show") ? "true" : "false");
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { menu.classList.remove("show"); });
    });
  }

  // FAQ accordions: <div class="faq-item"> with .faq-q and .faq-a
  document.querySelectorAll(".faq-q").forEach(function (q, index) {
    q.addEventListener("click", function (e) {
      var item = q.closest(".faq-item");
      var open = item.classList.contains("open");
      // Optional single-open behaviour if parent has data-single="true"
      if (q.closest(".faq[data-single='true']")) {
        q.closest(".faq").querySelectorAll(".faq-item.open").forEach(function (o) {
          o.classList.remove("open");
        });
      }
      if (!open) item.classList.add("open"); else item.classList.remove("open");
      var chev = q.querySelector(".chev");
      if (chev) chev.setAttribute("aria-expanded", open ? "false" : "true");
    });
  });

  // Smooth scroll for same-page anchor links pointing to #section
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (id.length < 2) return;
      var el = document.querySelector(id);
      if (el) { e.preventDefault(); el.scrollIntoView({ behavior: "smooth", block: "start" }); }
    });
  });

  // Lightweight scroll-reveal
  var revealEls = document.querySelectorAll("[data-reveal]");
  if (revealEls.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.style.opacity = 1;
          en.target.style.transform = "translateY(0)";
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el, i) {
      el.style.opacity = 0;
      el.style.transform = "translateY(14px)";
      el.style.transition = "opacity .6s ease, transform .6s ease";
      el.style.transitionDelay = (i % 3) * 0.06 + "s";
      io.observe(el);
    });
  }
})();
