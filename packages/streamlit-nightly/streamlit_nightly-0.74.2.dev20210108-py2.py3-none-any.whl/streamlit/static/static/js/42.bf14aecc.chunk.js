/*! For license information please see 42.bf14aecc.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[42],{3811:function(e,t,r){"use strict";r.r(t),r.d(t,"default",(function(){return s}));var n=r(1),a=r(0),c=r(12),i=r(56);function s(e){var t=e.element,r=e.width,s=Object(a.useRef)(null),o=t.type,u=t.url;Object(a.useEffect)((function(){var e=s.current,r=function(){e&&(e.currentTime=t.startTime)};return e&&e.addEventListener("loadedmetadata",r),function(){e&&e.removeEventListener("loadedmetadata",r)}}),[t]);if(o===c.r.Type.YOUTUBE_IFRAME){var l=.75*r;return Object(n.jsx)("iframe",{title:u,src:function(e){var r=t.startTime;return r?"".concat(e,"?start=").concat(r):e}(u),width:r,height:l,frameBorder:"0",allow:"autoplay; encrypted-media",allowFullScreen:!0})}return Object(n.jsx)("video",{ref:s,controls:!0,src:Object(i.b)(u),className:"stVideo",style:{width:r}})}}}]);
//# sourceMappingURL=42.bf14aecc.chunk.js.map