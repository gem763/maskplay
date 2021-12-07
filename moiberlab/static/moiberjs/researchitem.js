(function($) {
  $(function() {
    $('select[name*="type"]').change(function() {
      const value = $(this).val();
      const pix_0 = $(this).closest('.predefined').siblings('.pix_0');
      const pix_1 = $(this).closest('.predefined').siblings('.pix_1');
      const mc = $(this).closest('.predefined').siblings('.mc');

      switch(value) {
        case 'AB':
          pix_0.show();
          pix_1.show();
          mc.hide();
          break;

        case 'OX':
          pix_0.show();
          pix_1.hide();
          mc.hide();
          break;

        case 'QA':
          pix_0.show();
          pix_1.hide();
          mc.hide();
          break;

        case 'MC':
          pix_0.show();
          pix_1.hide();
          mc.show();
          break;

        case 'IN':
          pix_0.show();
          pix_1.hide();
          mc.hide();
          break;

        case 'OUT':
          pix_0.show();
          pix_1.hide();
          mc.hide();
          break;

      }
    });

    $('select[name*="type"]').trigger('change');
  });
})(django.jQuery);
