/*! For license information please see 29.524a53c5.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[29],{1178:function(e,t,n){"use strict";n.d(t,"a",(function(){return s})),n.d(t,"b",(function(){return a}));var r=n(7),i=n.n(r),a=i()("label",{target:"effi0qh0"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.bodyText,marginBottom:t.fontSizes.halfSmDefault}}),""),s=i()("div",{target:"effi0qh1"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.gray,margin:t.spacing.none,textAlign:"right",position:"absolute",bottom:0,right:t.fontSizes.halfSmDefault}}),"")},3793:function(e,t,n){"use strict";n.r(t),n.d(t,"default",(function(){return ue}));var r,i,a=n(1),s=n(231),o=n(10),l=n(22),c=n(23),u=n(0),d=n.n(u),f=n(153),g=n.n(f),p=n(42);!function(e){e.ERROR="ERROR",e.DELETING="DELETING",e.READY="READY",e.UPLOADING="UPLOADING",e.UPLOADED="UPLOADED"}(r||(r={})),function(e){e.GigaByte="gb",e.KiloByte="kb",e.MegaByte="mb",e.Byte="b"}(i||(i={}));var m=Object(p.g)()?1024:1e3,h=[i.GigaByte,i.MegaByte,i.KiloByte,i.Byte],j=function e(t,n){var r=arguments.length>2&&void 0!==arguments[2]?arguments[2]:1;if(n||(n=i.Byte),r<0&&(r=0),t<0)throw new Error("Size must be greater than or equal to 0");var a=h.indexOf(n),s=t/m;return a&&t>m/2?e(s,h[a-1],r):"".concat(t.toFixed(r)).concat(n.toUpperCase())},x=function(e,t,n){if(e<0)throw Error("Size must be 0 or greater");var r=h.findIndex((function(e){return e===t})),i=h.findIndex((function(e){return e===n}));if(-1===r||-1===i)throw Error("Unexpected byte unit provided");if(r===i)return e;var a=Math.abs(r-i),s=Math.pow(m,a);return r>i?e/s:e*s},b=n(1178),v=n(43),O=n(6),y=n(2459),S=n.n(y),D=n(20),E=n(7),z=n.n(E);var R,w=z()("section",{target:"exg6vvm0"})((function(e){var t=e.isDisabled,n=e.theme;return{display:"flex",alignItems:"center",padding:n.spacing.lg,backgroundColor:n.inSidebar?n.colors.white:n.colors.lightestGray,borderRadius:n.radii.md,":focus":{outline:"none",boxShadow:"0 0 0 1px ".concat(n.colors.primary)},color:t?n.colors.gray:n.colors.bodyText}}),""),B=z()("div",{target:"exg6vvm1"})((function(e){e.theme;return{marginRight:"auto",alignItems:"center",display:"flex"}}),""),F=z()("span",{target:"exg6vvm2"})((function(e){var t=e.theme;return{color:t.colors.secondary,marginRight:t.spacing.lg}}),""),M=z()("span",{target:"exg6vvm3"})((function(e){return{marginBottom:e.theme.spacing.twoXS}}),""),A=z()("div",{target:"exg6vvm4"})({name:"j7qwjs",styles:"display:flex;flex-direction:column;"}),k=z()("div",{target:"exg6vvm5"})((function(e){var t=e.theme;return{left:0,right:0,lineHeight:t.lineHeights.tight,paddingTop:t.spacing.md,paddingLeft:t.spacing.lg,paddingRight:t.spacing.lg}}),""),I=z()("ul",{target:"exg6vvm6"})((function(e){e.theme;return{listStyleType:"none"}}),""),C=z()("li",{target:"exg6vvm7"})((function(e){var t=e.theme;return{margin:t.spacing.none,padding:t.spacing.none}}),""),L=z()("div",{target:"exg6vvm8"})((function(e){return{display:"flex",alignItems:"baseline",flex:1,paddingLeft:e.theme.spacing.lg,overflow:"hidden"}}),""),N=z()("div",{target:"exg6vvm9"})((function(e){var t=e.theme;return{marginRight:t.spacing.sm,marginBottom:t.spacing.twoXS,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}),""),U=z()("div",{target:"exg6vvm10"})((function(e){return{display:"flex",alignItems:"center",marginBottom:e.theme.spacing.twoXS}}),""),P=z()("span",{target:"exg6vvm11"})((function(e){return{marginRight:e.theme.spacing.twoXS}}),""),T=z()("div",{target:"exg6vvm12"})((function(e){var t=e.theme;return{display:"flex",padding:t.spacing.twoXS,color:t.colors.secondary}}),""),G=z()("small",{target:"exg6vvm13"})((function(e){var t=e.theme;return{color:t.colors.danger,fontSize:t.fontSizes.smDefault,height:t.fontSizes.smDefault,lineHeight:t.fontSizes.smDefault,display:"flex",alignItems:"center",whiteSpace:"nowrap"}}),""),Y=z()("span",{target:"exg6vvm14"})({name:"0",styles:""}),X=function(e){return{[w]:{display:"flex",flexDirection:"column",alignItems:"flex-start"},[B]:{marginBottom:e.spacing.lg},[F]:{display:"none"},[k]:{paddingRight:e.spacing.lg},[U]:{maxWidth:"inherit",flex:1,alignItems:"flex-start",marginBottom:e.spacing.sm},[N]:{width:e.sizes.full},[L]:{flexDirection:"column"},[G]:{height:"auto",whiteSpace:"initial"},[Y]:{display:"none"},[C]:{margin:e.spacing.none,padding:e.spacing.none}}},q=z()("div",{target:"exg6vvm15"})((function(e){var t=e.theme;return t.inSidebar?X(t):{["@media (max-width: ".concat(t.breakpoints.sm,")")]:X(t)}}),""),H=n(1499),J=n(70);!function(e){e.SECONDARY="secondary",e.DANGER="danger"}(R||(R={}));var K=z()("small",{target:"euu6i2w0"})((function(e){var t=e.kind,n=e.theme,r=t===R.SECONDARY&&n.colors.secondary;return{color:t===R.DANGER&&n.colors.danger||r||n.colors.darkGray,fontSize:n.fontSizes.smDefault,height:n.fontSizes.smDefault,lineHeight:n.fontSizes.smDefault,display:"flex",alignItems:"center"}}),""),W=function(e){var t=e.multiple,n=e.acceptedExtensions,r=e.maxSizeBytes;return Object(a.jsxs)(B,{children:[Object(a.jsx)(F,{children:Object(a.jsx)(J.a,{content:H.CloudUpload,size:"threeXL"})}),Object(a.jsxs)(A,{children:[Object(a.jsxs)(M,{children:["Drag and drop file",t?"s":""," here"]}),Object(a.jsxs)(K,{children:["Limit ".concat(j(r,i.Byte,0)," per file"),n.length?" \u2022 ".concat(n.join(", ").replace(/\./g,"").toUpperCase()):null]})]})]})},Q=function(e){var t=e.onDrop,n=e.multiple,r=e.acceptedExtensions,i=e.maxSizeBytes,s=e.disabled;return Object(a.jsx)(S.a,{onDrop:t,multiple:n,accept:r.length?r:void 0,maxSize:i,disabled:s,children:function(e){var t=e.getRootProps,o=e.getInputProps;return Object(a.jsxs)(w,Object(O.a)(Object(O.a)({},t()),{},{"data-testid":"stFileUploadDropzone",isDisabled:s,children:[Object(a.jsx)("input",Object(O.a)({},o())),Object(a.jsx)(W,{multiple:n,acceptedExtensions:r,maxSizeBytes:i}),Object(a.jsx)(D.c,{kind:D.a.PRIMARY,disabled:s,size:D.b.SMALL,children:"Browse files"})]}))}})},V=n(44),Z=n(141),$=n(82),_=n.n($),ee=z()("div",{target:"e1f8s2qs0"})((function(e){var t=e.theme;return{display:"flex",alignItems:"center",justifyContent:"space-between",paddingBottom:t.spacing.twoXS,marginBottom:t.spacing.twoXS}}),""),te=z()("div",{target:"e1f8s2qs1"})((function(e){return{display:"flex",alignItems:"center",justifyContent:"center",color:e.theme.colors.secondary}}),""),ne=function(e){var t=e.className,n=e.currentPage,r=e.totalPages,i=e.onNext,s=e.onPrevious;return Object(a.jsxs)(ee,{className:t,children:[Object(a.jsx)(K,{children:"Showing page ".concat(n," of ").concat(r)}),Object(a.jsxs)(te,{children:[Object(a.jsx)(D.c,{onClick:s,kind:D.a.MINIMAL,children:Object(a.jsx)(J.a,{content:H.ChevronLeft,size:"xl"})}),Object(a.jsx)(D.c,{onClick:i,kind:D.a.MINIMAL,children:Object(a.jsx)(J.a,{content:H.ChevronRight,size:"xl"})})]})]})},re=function(e,t){return Math.ceil(e.length/t)},ie=function(e){return _()((function(t){var n=t.pageSize,r=t.items,i=t.resetOnAdd,s=Object(Z.a)(t,["pageSize","items","resetOnAdd"]),o=Object(u.useState)(0),l=Object(V.a)(o,2),c=l[0],d=l[1],f=Object(u.useState)(re(r,n)),g=Object(V.a)(f,2),p=g[0],m=g[1],h=function(e){var t=Object(u.useRef)();return Object(u.useEffect)((function(){t.current=e}),[e]),t.current}(r);Object(u.useEffect)((function(){h&&h.length!==r.length&&m(re(r,n)),h&&h.length<r.length?i&&d(0):c+1>=p&&d(p-1)}),[r,c,n,h,i,p]);var j=r.slice(c*n,c*n+n);return Object(a.jsxs)(a.Fragment,{children:[Object(a.jsx)(e,Object(O.a)({items:j},s)),r.length>n?Object(a.jsx)(ne,{className:"streamlit-paginator",pageSize:n,totalPages:p,currentPage:c+1,onNext:function(){d(Math.min(c+1,p-1))},onPrevious:function(){d(Math.max(0,c-1))}}):null]})}),e)},ae=n(236),se=function(e){var t=e.file,n=e.progress;return n?Object(a.jsx)(ae.b,{value:n,size:ae.a.SMALL,overrides:{Bar:{style:{marginLeft:0,marginTop:"4px"}}}}):t.status===r.ERROR?Object(a.jsxs)(G,{children:[Object(a.jsx)(P,{"data-testid":"stUploadedFileErrorMessage",children:t.errorMessage||"error"}),Object(a.jsx)(Y,{children:Object(a.jsx)(J.a,{content:H.Error,size:"lg"})})]}):t.status===r.UPLOADED?Object(a.jsx)(K,{kind:R.SECONDARY,children:j(t.size,i.Byte)}):t.status===r.DELETING?Object(a.jsx)(K,{kind:R.SECONDARY,children:"Removing file"}):null},oe=function(e){var t=e.file,n=e.progress,r=e.onDelete;return Object(a.jsxs)(U,{className:"uploadedFile",children:[Object(a.jsx)(T,{children:Object(a.jsx)(J.a,{content:H.InsertDriveFile,size:"twoXL"})}),Object(a.jsxs)(L,{className:"uploadedFileData",children:[Object(a.jsx)(N,{className:"uploadedFileName",title:t.name,children:t.name}),Object(a.jsx)(se,{file:t,progress:n})]}),Object(a.jsx)(D.c,{onClick:function(){return r(t.id||"")},kind:D.a.MINIMAL,children:Object(a.jsx)(J.a,{content:H.Clear,size:"lg"})})]})},le=ie((function(e){var t=e.items,n=e.onDelete;return Object(a.jsx)(I,{children:t.map((function(e){return Object(a.jsx)(C,{children:Object(a.jsx)(oe,{file:e,progress:e.progress,onDelete:n})},e.id)}))})})),ce=function(e){return Object(a.jsx)(k,{children:Object(a.jsx)(le,Object(O.a)({},e))})},ue=function(e){Object(l.a)(n,e);var t=Object(c.a)(n);function n(e){var l;Object(o.a)(this,n),(l=t.call(this,e)).componentDidUpdate=function(e){e.disabled!==l.props.disabled&&l.props.disabled&&l.reset();var t=l.props.element.maxUploadSizeMb;e.element.maxUploadSizeMb!==t&&l.setState({maxSizeBytes:x(t,i.MegaByte,i.Byte)})},l.reset=function(){l.setState({status:r.READY,errorMessage:void 0,files:[]})},l.dropHandler=function(e,t){var n=l.props.element.multipleFiles;if(!n&&l.state.files.length&&l.removeFile(l.state.files[0].id||""),l.props.uploadClient.updateFileCount(l.props.element.id,n?l.state.files.length+e.length:1),t.length>1&&!n){var r=t.findIndex((function(e){return 1===e.errors.length&&"too-many-files"===e.errors[0].code}));if(r>=0){var i=t[r];l.uploadFile(i.file,e.length),l.rejectFiles([].concat(Object(s.a)(t.slice(0,r)),Object(s.a)(t.slice(r+1))))}else l.rejectFiles(t)}else l.rejectFiles(t);e.map(l.uploadFile)},l.handleFile=function(e,t){return e.id="".concat(t).concat((new Date).getTime()),e.cancelToken=g.a.CancelToken.source(),l.setState((function(t){return{files:[e].concat(Object(s.a)(t.files))}})),e},l.uploadFile=function(e,t){e.progress=1,e.status=r.UPLOADING;var n=l.handleFile(e,t);l.props.uploadClient.uploadFiles(l.props.element.id,[e],(function(e){return l.onUploadProgress(e,n.id)}),e.cancelToken?e.cancelToken.token:g.a.CancelToken.source().token,!l.props.element.multipleFiles).then((function(){l.setState((function(t){return{files:t.files.map((function(t){return e.id===t.id?(delete e.progress,delete e.cancelToken,e.status=r.UPLOADED,e):t}))}}))})).catch((function(e){g.a.isCancel(e)||l.setError(e?e.toString():"Unknown error")}))},l.rejectFiles=function(e){e.forEach((function(e,t){Object.assign(e.file,{status:r.ERROR,errorMessage:l.getErrorMessage(e.errors[0].code,e.file)}),l.handleFile(e.file,t)}))},l.getErrorMessage=function(e,t){switch(e){case"file-too-large":return"File must be ".concat(j(l.state.maxSizeBytes,i.Byte)," or smaller.");case"file-invalid-type":return"".concat(t.type," files are not allowed.");case"file-too-small":return"File size is too small.";case"too-many-files":return"Only one file is allowed.";default:return"Unexpected error. Please try again."}},l.setError=function(e){l.setState({status:r.ERROR,errorMessage:e})},l.delete=function(e){var t=l.state.files.find((function(t){return t.id===e}));if(e&&t){if(t.errorMessage)return void l.removeFile(e);t.cancelToken&&t.cancelToken.cancel(),l.props.uploadClient.delete(l.props.element.id,e).then((function(){return l.removeFile(e)}),(function(t){404===t.response.status&&l.removeFile(e)}))}else l.setError("File not found. Please try again.")},l.removeFile=function(e){l.setState((function(t){var n=t.files.filter((function(t){return t.id!==e}));return{status:n.length?r.UPLOADED:r.READY,errorMessage:void 0,files:n}}),(function(){return l.props.uploadClient.updateFileCount(l.props.element.id,l.state.files.length)}))},l.onUploadProgress=function(e,t){var n=Math.round(100*e.loaded/e.total),r=l.state.files.find((function(e){return e.id===t}));r&&r.progress!==n&&(r.progress=n,l.setState((function(e){return{files:e.files.map((function(e){return e.id===t?r:e}))}})))},l.render=function(){var e=l.state,t=e.maxSizeBytes,n=e.errorMessage,r=e.files,i=l.props,o=i.element,c=i.disabled,u=o.type;return Object(a.jsxs)(q,{"data-testid":"stFileUploader",children:[Object(a.jsx)(b.b,{children:o.label}),n?Object(a.jsx)(v.b,{kind:v.a.ERROR,children:n}):null,Object(a.jsx)(Q,{onDrop:l.dropHandler,multiple:o.multipleFiles,acceptedExtensions:u,maxSizeBytes:t,disabled:c}),Object(a.jsx)(ce,{items:Object(s.a)(r),pageSize:3,onDelete:l.delete,resetOnAdd:!0})]})};var c=e.element.maxUploadSizeMb;return l.state={status:"READY",errorMessage:void 0,files:[],maxSizeBytes:x(c,i.MegaByte,i.Byte)},l}return n}(d.a.PureComponent)}}]);
//# sourceMappingURL=29.524a53c5.chunk.js.map