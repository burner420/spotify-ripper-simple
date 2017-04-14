




// MODEL

Rip = Backbone.Model.extend({
    initialize: function() {
        console.log("Rip initialied");
    },
    urlRoot: "/api/rip",
    url: function() {
        var base = this.urlRoot || (this.collection && this.collection.url) || "/";
        if (this.isNew()) return base;
        return base + "/" + encodeURIComponent(this.id);
    }
});



/// Collection

var Rips = Backbone.Collection.extend({
	initialize: function() {
		console.log("Rips Collection is initialized");
	},
	url:"/api/rip",
	model: Rip
});







/// Views

var RipsView = Backbone.View.extend({
    initialize: function () {
        console.log("Rips View - Initialized");
    },
    el: '#rip-list',
    render: function() {
        console.log('Rips View - Rendered');
        console.log(this.$el);
        this.ripViews={};
        this.collection.each(function(rip){
            var rv = new RipView({model:rip});
            rv.render();
            this.$el.append(rv.el);
            this.ripViews[rip.id] = rv;
	    },this);
    },
    update: function(){
        this.collection.each(function(rip){
            this.ripViews[rip.id].update(rip);
	    },this);
    }
});





var RipView = Backbone.View.extend({
    template: _.template( $('#rip-template').html() ),
    initialize: function () {
        console.log("Rip View - Initialized");
    },

    render: function() {
        this.lastModelData = this.model.toJSON();
        this.$el.html(this.template(this.lastModelData));
        this.setTimeRemaining(true);
        this.setProgress(true);
        this.setDownloadButton(true);
        this.setStatusIcon(true);
        this.setSongList(true);
    },
    events: {
      'click .rip-item-details-toggle': 'toggleDetails'
    },
    toggleDetails: function(){

        var section = this.$el.find(".rip-item-details").first();
        var button = this.$el.find(".rip-item-details-toggle").first();
        if( section.is(":visible") ){
            section.hide();
            button.removeClass("glyphicon-minus");
            button.addClass("glyphicon-plus");
        }else{
            section.show();
            button.removeClass("glyphicon-plus");
            button.addClass("glyphicon-minus");
        }

    },
    update: function(rip){
        this.setTimeRemaining();
        this.setProgress();
        this.setDownloadButton();
        this.setStatusIcon();
        this.setSongList();
        this.lastModelData = this.model.toJSON();
    },
    setTimeRemaining: function(initialRender){
        if (typeof(initialRender)==='undefined') initialRender = false;
        var section = this.$el.find(".time-remaining").first();
        if (this.model.get("status") == 2){
            section.html( this.model.get("total_eta_formatted") + " Remaining" );
        }else{
            section.html("");
        }

    },
    setProgress: function(initialRender){
        if (typeof(initialRender)==='undefined') initialRender = false;
        var progress = this.$el.find(".progress-bar-section").first();
        if (this.model.get("status") == 2){
            progress.html('<div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="" aria-valuemin="0" aria-valuemax="100" style="width: '+ this.model.get("total_pct") +'%;">'+ this.model.get("total_pct") +'%</div></div>');
        }else{
            progress.html("");
        }

    },
    setDownloadButton: function(initialRender){
        if (typeof(initialRender)==='undefined') initialRender = false;
        var iconHtml = '<span class="glyphicon glyphicon glyphicon-save"></span>';
        var inactive = '<span class="glyphicon glyphicon glyphicon-save grey"></span>';
        var section = this.$el.find(".rip-item-save-icon-span").first();
        if (this.model.get("status") == 3){
            section.html('<a href="/download/'+this.model.get('file_name')+'">'+iconHtml+'</a>');
        }else{
            section.html(inactive);
        }
    },
    setStatusIcon: function(initialRender){
        if (typeof(initialRender)==='undefined') initialRender = false;

        var status = this.model.get('status');
        var default_ = '<span class="glyphicon glyphicon glyphicon-ok-sign"></span>';
        var queued = '<span class="glyphicon glyphicon glyphicon-time"></span>';
        var rotate = '<span class="glyphicon glyphicon glyphicon-refresh rotate"></span>';
        var success = '<span class="glyphicon glyphicon glyphicon-ok-sign green"></span>';
        var error = '<span class="glyphicon glyphicon glyphicon-warning-sign red"></span>';
        if(status == this.lastModelData.status && initialRender == false){
            return;
        }
        var section = this.$el.find(".rip-item-status-icon-span").first();
        var errorSection = this.$el.find(".error-list").first();

        if (this.model.get("status") == 1){
            section.html(queued);
        }
        else if (this.model.get("status") == 2){
            section.html(rotate);
        }else if(this.model.get("status") == 3) {
            section.html(success);
            if(this.lastModelData.status < 3 ){
                var ding = new Audio('/static/ding.wav');
                ding.play();
            }
        }else if(this.model.get("status") == 4) {
            section.html(error);
            errorSection.html('<div class="alert alert-warning" role="alert">An error occured.</div>');
        }else if(this.model.get("status") == 5) {
            section.html(error);
            errorSection.html('<div class="alert alert-danger" role="alert">Error logging in. Try updating your username and/or password on the <a href="/setup">Setup Page</a>.</div>');
        }else if(this.model.get("status") == 6) {
            section.html(error);
            errorSection.html('<div class="alert alert-danger" role="alert">Bad app key.  Upload a valid app key in the <a href="/setup">Setup Page</a>.</div>');
        }
        else{
            section.html(default_);
        }
    },
    setSongList: function(initialRender){
        if (typeof(initialRender)==='undefined') initialRender = false;

        var sectionHtml = '';
        var section = this.$el.find(".song-list").first();
        var songs = this.model.get('songs');

        if(this.lastModelData.songs.length == songs.length && initialRender == false){
            return;
        }
        sectionHtml += "<h3>Songs ("+ songs.length +")</h3>";
        _.each(songs, function(song){
            sectionHtml += '<p class="song">' + song.artist + ' - ' + song.name + '</p>';
	    },this);
        section.html(sectionHtml);
    }
});










$(function() {
    rips = new Rips();
    console.log(rips);
    var ripsView = new RipsView({ collection: rips });
    rips.fetch({ success: function () { ripsView.render();; } });

    window.setInterval(function(){ rips.fetch(); }, 2000);
    rips.on('change', function () {
        ripsView.update();
    });
    $(".alert-dismissible").fadeTo(2000, 500).slideUp(500, function(){
        $(".alert-dismissible").slideUp(500);
    });
});
