define(['react', 'underscore', 'components/page_header', 
    'collections/applications', 'components/common/gravatar', 'router',
    'components/common/rating'],
    function(React, _, PageHeader, Applications, Gravatar, router, Rating) {

    var Bookmark = React.createClass({
        getInitialState: function() {
            return {
                isFavorite: this.props.image.get('favorite')
            };
        },
        updateFavorite: function(model) {
            this.setState({'isFavorite': model.get('favorite')});
        },
        componentDidMount: function() {
            this.props.image.on('change:favorite', this.updateFavorite);
        },
        componentWillUnmount: function() {
            this.props.image.off('change:favorite', this.updateFavorite);
        },
        toggleFavorite: function(e) {
            e.preventDefault();
            this.props.image.set('favorite', !this.props.image.get('favorite'));
        },
        render: function() {
            return React.DOM.a({
                className: 'bookmark ' + (this.state.isFavorite ? 'on' : 'off'),
                href: '#',
                onClick: this.toggleFavorite
            });
        }
    });

    var ApplicationPreview = React.createClass({
        onImageClick: function(e) {
            e.preventDefault();
            router.navigate("images/" + this.props.application.id, {trigger: true});
        },
        render: function() {
            var app = this.props.application;

            var iconSize = 150;
            var icon;
            if (app.get('icon'))
                icon = React.DOM.img({
                    src: app.get('icon'),
                    width: iconSize,
                    height: iconSize
                });
            else
                icon = Gravatar({hash: app.get('uuid_hash'), size: iconSize});

            var imageUri = "images/" + app.get('uuid');

            return React.DOM.li({}, 
                React.DOM.div({className: 'icon-container'}, React.DOM.a({
                        href: imageUri, 
                        onClick: this.onImageClick
                    }, icon)),
                React.DOM.div({className: 'app-name'}, React.DOM.a({
                        href: imageUri, 
                        onClick: this.onImageClick,
                        title: app.get('name_or_id')
                    }, app.get('name_or_id'))),
                Rating({rating: app.get('rating')}),
                Bookmark({image: app}));
        }
    });

    var ApplicationPreviewList = React.createClass({
        render: function() {
            var apps = this.props.applications;
            return React.DOM.div({},
                React.DOM.h2({}, this.props.title),
                React.DOM.ul({className: 'app-preview-list'}, apps.map(function(app) {
                    return ApplicationPreview({application: app});
                })));
        }
    });

    var ApplicationsHome = React.createClass({
        getInitialState: function() {
            return {
                applications: null
            };
        },
        helpText: function() {
            return React.DOM.p({}, "Applications are cool. You are, too. Keep bein' cool, bro.");
        },
        render: function() {
            var content = React.DOM.div({}, "loading");
            if (this.state.applications != null)
                content = [ApplicationPreviewList({
                    title: "Featured Images",
                    applications: new Applications(this.state.applications.filter(function(app) {
                        return app.get('featured');
                    }))
                })];

            return React.DOM.div({},
                PageHeader({title: 'Images', helpText: this.helpText}),
                content);
        },
        updateApplications: function(apps) {
            if (this.isMounted())
                this.setState({applications: apps});
        },
        componentDidMount: function() {
            var apps = new Applications();
            apps.on('sync', this.updateApplications);
            apps.fetch();
        },
        componentWillUnmount: function() {
            if (this.state.applications)
                this.state.applications.off('sync', this.updateApplications);
        }
    });

    return ApplicationsHome;

});
