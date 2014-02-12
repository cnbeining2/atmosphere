define(['backbone', 'react'], function(Backbone, React) {
    var Router = Backbone.Router.extend({
        routes: {
            '': 'handleDefaultRoute',
            'dashboard': 'dashboard',
            'images': 'images',
            'images/favorites': 'imageFavorites',
            'images/authored': 'imageAuthored',
            'images/:id': 'imageDetail',
            'instances': 'instances',
            'volumes': 'volumes',
            'providers': 'providers',
            'settings': 'settings',
            'help': 'help'
        },
        setDefaultRoute: function(route) {
            this.defaultRoute = route;
        },
        handleDefaultRoute: function() {
            this.navigate(this.defaultRoute, {trigger: true, replace: true});
        },
        setView: function(requirements, getView) {
            var node = document.getElementById('main');
            var loading = React.DOM.div({className: 'loading'});
            React.renderComponent(loading, node);
            require(requirements, function() {
                var modules = arguments;
                React.renderComponent(getView.apply(this, modules),
                    node);
            }.bind(this));
        },
        dashboard: function() {
            this.setView(['components/dashboard'], function(Dashboard) {
                return Dashboard();
            });
        },
        images: function() {
            this.setView(['components/images'], function(Images) {
                console.log(arguments);
                return Images();
            });
        },
        imageFavorites: function() {
        },
        imageAuthored: function() {
        },
        imageDetail: function(id) {
            this.setView(['components/image_detail'], function(ImageDetail) {
                return ImageDetail({image_id: id});
            });
        },
        instances: function() {
            this.setView(['components/instances'], function(Instances) {
                return Instances();
            });
        },
        volumes: function() {
            this.setView(['components/volumes'], function(Volumes) {
                return Volumes();
            });
        },
        providers: function() {
            this.setView(['components/providers'], function(Providers) {
                return Providers();
            });
        },
        settings: function() {
            this.setView(['components/settings'], function(Settings) {
                return Settings();
            });
        },
        help: function() {
            this.setView(['components/help'], function(Help) {
                return Help();
            });
        }
    });

    return new Router();
});
