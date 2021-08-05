django.jQuery( document ).ready(function() {

  django.jQuery('input').change(function() {

    if (this.files[0]){
      const self = this;
      const reader = new FileReader();
      reader.readAsDataURL(this.files[0]);

      reader.onload = function(e){
          django.jQuery(self).closest('div.img_container').children('img.preview').attr('src', e.target.result).show();
          django.jQuery(self).closest('div.img_container').children('img.current').hide();

          // django.jQuery(self).siblings('img.preview').attr('src', e.target.result).show();
          // django.jQuery(self).siblings('img.current').hide();
      };
    }
  });
});
