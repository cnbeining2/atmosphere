define(['react', 'profile'], function(React, profile) {

    var Icon = React.createClass({
        propTypes: {
            hash: React.PropTypes.string
        },
        getSrc: function(hash, icon_set) {
            switch (icon_set) {
                case 'unicorn':
                    return "//unicornify.appspot.com/avatar/" + hash + "?s=50";
                case 'wavatar':
                    return "//www.gravatar.com/avatar/" + hash + "?d=wavatar&s=50";
                case 'monster':
                    return "//www.gravatar.com/avatar/" + hash + "?d=monsterid&s=50";
                case 'retro':
                    return "//www.gravatar.com/avatar/" + hash + "?d=retro&s=50";
                case 'robot':
                    return "//robohash.org/" + hash + "?size=50x50";
                default:
                    return "//www.gravatar.com/avatar/" + hash + "?d=identicon&s=50"; 
            }
        },
        render: function() {
            /* If a type is specified in props, use it. Otherwise, use the 
             * profile setting 
             */
            var icon_set = this.props.type;
            if (!icon_set)
                icon_set = profile.get('settings')['icon_set'];
            return React.DOM.img({src: this.getSrc(this.props.hash, icon_set)});
        }
    });

    return Icon;

});
