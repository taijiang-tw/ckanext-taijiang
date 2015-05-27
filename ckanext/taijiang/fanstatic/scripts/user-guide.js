this.ckan.module('intro-action', function (jQuery, _) {
  return {
    /* An object of module options */
    options: {
      /* Locale options can be overidden with data-module-i18n attribute */
      i18n: {
        keywordSearch: _('Here you can search datasets by a keyword.'),
        spatialSearch: _('Here you can search datasets by the map.'),
        temporalSearch: _('Here you can search datasets by a period of time.'),
        filter: _('Here you can filter datasets.'),
        datasetList: _('The matched datasets will list here.'),
        showHelp: _('Click this question mark to show this help again.'),
        skip: _('Skip'),
        done: _('Confirm')
      },
       template: [
         '<i id="intro-switch" class="icon-question-sign icon-large pull-right">',
         '</i>'
       ].join('\n')
    },

    initialize: function () {
      intro = introJs();
      var introStart = true;
      var visited = localStorage.getItem('taijiang-dataset-intro');
      introStart = visited ? false : true;
      var md = new MobileDetect(window.navigator.userAgent);
      var isMobile = md.mobile() ? true : false;

      intro.setOptions({
        overlayOpacity: 0.5,
        nextLabel: ' &rarr; ',
        prevLabel: '&larr; ',
        showStepNumbers: false,
        skipLabel: this.i18n('skip'),
        doneLabel: this.i18n('done'),
        steps: [
          {
            element: '.search-input',
            intro: this.i18n('keywordSearch')
          },
	  {
	    element: '#dataset-map',
	    intro: this.i18n('spatialSearch'),
	    position: 'right'
	  },
          {
            element: '[data-module="date-facet"]',
            intro: this.i18n('temporalSearch'),
            position: 'right'
          },
          {
            element: '#facets',
            intro: this.i18n('filter'),
            position: 'right'
          },
          {
            element: '.dataset-list',
            intro: this.i18n('datasetList'),
            position: 'right'
          },
          {
            element: '#intro-switch',
            intro: this.i18n('showHelp'),
            position: 'right'
          }
        ]
      });

      if(isMobile) {
        introStart = false;
      } else {
        this.createMark().appendTo('.breadcrumb .active');
	this.mark.css({
          'cursor': 'pointer',
	  'color': '#d9534f'
        });
	this.mark.on('click', this._onClick);
      }

      if(introStart) {
        localStorage.setItem('taijiang-dataset-intro', 1);
        intro.start();
      }
    },

    createMark: function () {
      if (!this.mark) {
        var element = this.mark = jQuery(this.options.template);
      }
      return this.mark;
    },

    _onClick: function(event) {
      intro.start();
    }
  }
});
