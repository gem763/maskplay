const guestboo = 363;

class Session {
  constructor() {
    this.page = {
      my:           { open: false },
      agit:         { open: false, boo: undefined, from: 'left' },
      finder:       { open: false, from: 'left', collections: undefined },
      collector:    { open: false, from: 'bottom', pix: undefined },
      login:        { open: false, from: 'left' },
      about:        { open: false, from: 'left', section: 'who' },
      texteditor:   { open: false, basetext: undefined, setter: undefined, placeholder: undefined, maxlines: 1 },
      pixeditor:    { open: false, src: undefined, pixloader: undefined, type: undefined },
      profiler:     { open: false, from: 'left', type: undefined },
      landing:      { open: false, from: 'left' },

      mbti:         { open: false, from: 'left', contents: undefined },
      mbtiresult:   { open: false, from: 'left', result: undefined, gender: undefined, mode: undefined },

      // home:       { open: false, from: 'left', hotboos: new Boos('hot') },
      // posts:      { open: true, contents: undefined, univ: { hot: new Posts('hot'), history: new Posts('history'), custom: undefined, search: undefined }, swiper: undefined },
      // mypage:     { open: false, from: 'left' },
      // loginpage:  { open: false, from: 'bottom' },
      // navigator:  { open: false, from: 'left' },
      // profiler:   { open: false, from: 'right', type: undefined },
      // boopage:    { open: false, from: 'left', boo: undefined },
      // network:    { open: false, from: 'right', type: undefined, boos_group: undefined },
      // posting:    { open: false, from: 'right', post: undefined, type: undefined },
      // comments:   { open: false, from: 'right', post: undefined },
      // booposts:   { open: false, from: 'right', open_at: 0, swiper: undefined },
      // pixeditor:  { open: false, src: undefined, pixloader: undefined, type: undefined },
      // bridge:     { open: false, from: undefined, type: undefined, callback: undefined, args: undefined },
      // searcher:   { open: false, from: 'right' },
      // company:    { open: false, from: 'right', section: 'who' },
      // landing:    { open: false, from: 'right' },
      // infoboard:  { open: false, from: 'right', contents: undefined },
    };

    this.store = new Store();
    this.editing = { on: false, selected:[] };
    this.pixtory = [{ pixs: new Pixs(this.store) }];
    this.scroll_direction = 'up';
    this.mode = { on: 'home', order: 0, prev: undefined };
    this.ikeyset = undefined;
    this.labels = undefined;
    this.entry = undefined;
    this.user = new User(this);
    this.keyset_sampling();
  }

  keyset_sampling() {
    this.ikeyset = _.sample([0, 1, 2]);
  }

  refresh() {
    this.keyset_sampling();
    this.pixtory = [{ pixs: new Pixs(this.store) }];
  }

  keywording(keyword) {
    this.pixtory = [{ pixs: new Searchpixs_by_keyword(this.store, keyword) }];
    // this.pixtory.push({ pixs: new Searchpixs_by_keyword(this.store, keyword) });
  }

  logout() {
    this.close_page();
    this.expire();

    fetch('/logout/')
      .then(x => {
        if (x.ok) {
          console.log('successfully logged out');
        }
      });
  }

  expire() {
    // auth만 제거하고, guest는 상주하게 한다
    this.user.auth = undefined;
  }

  close_page() {
    this.page[this.mode.on].open = false;
    this.checkout();
  }

  close_pages_all() {
    while (this.mode.on!='home') {
      this.close_page();
    }
  }

  open_page(pagename) {
    this.page[pagename].open = true;
    this.checkin(pagename);
  }

  checkin(on) {
    console.log(`check-in to ${on}`);
    this.mode.prev = {...this.mode};
    this.mode.on = on;
    this.mode.order = this.mode.prev.order + 1;
  }

  checkout() {
    try {
      console.log(`check-out from ${this.mode.on}, back to ${this.mode.prev.on}`)
      this.mode = this.mode.prev;

    } catch(e) {
      console.log('abnormal access')
    }
  }

  open_finder() {
    this.close_pages_all();
    this.open_page('finder');
  }

  open_login() {
    this.open_page('login');
  }

  open_my() {
    this.close_pages_all();

    if (this.user.auth) {
      this.open_agit(this.user.boo);

    } else {
      this.open_login();
    }
  }

  open_collector(pix) {
    this.page.collector.pix = pix;
    this.open_page('collector');
  }

  open_agit(boo) {
    this.page.agit.boo = boo;
    // agit 최초 오픈시 처음에는 boo=undefined 이기 때문에,
    // 열림효과가 제대로 반영하기 위해 약간 딜레이를 줬다
    setTimeout(() => { this.open_page('agit'); }, 10);
  }

  open_about(section) {
    if (section) {
      this.page.about.section = section;

    } else {
      this.page.about.section = 'who';
    }

    this.close_pages_all();
    this.open_page('about');
  }

  open_texteditor(basetext, placeholder, maxlines, setter) {
    this.page.texteditor.basetext = basetext;
    this.page.texteditor.placeholder = placeholder;
    this.page.texteditor.setter = setter;
    this.page.texteditor.maxlines = maxlines;
    this.open_page('texteditor');
  }

  open_pixeditor(src, type, pixloader) {
    this.page.pixeditor.src = src;
    this.page.pixeditor.type = type;
    this.page.pixeditor.pixloader = pixloader;
    this.open_page('pixeditor');
  }

  open_mbti() {
    if (!this.page.mbti.contents) {
      this.page.mbti.contents = new Mbti(this.store, 'dongne');
    }

    this.close_pages_all();
    this.open_page('mbti');
  }

  open_mbtiresult(result, gender, mode) {
    this.page.mbtiresult.result = result;
    this.page.mbtiresult.gender = gender;
    this.page.mbtiresult.mode = mode;
    this.open_page('mbtiresult');
  }

  open_landing() {
    // this.close_pages_all();
    this.open_page('landing');
  }

  open_profiler(type) {
    if (type) {
      this.page.profiler.type = type;

    } else {
      this.page.profiler.type = undefined;
    }

    this.open_page('profiler');
  }

  // open_mypage() {
  //   this.close_pages_all();
  //
  //   if (this.user.auth) {
  //     this.open_page('mypage');
  //
  //   } else {
  //     this.open_bridge('login_guide_for_mypage', 'bottom');
  //   }
  // }
  //
  // open_bridge(type, from, callback, args) {
  //   this.page.bridge.type = type;
  //   this.page.bridge.from = from;
  //   this.page.bridge.callback = callback;
  //   this.page.bridge.args = args;
  //   this.open_page('bridge');
  // }
  //
  // open_boochooser() {
  //   this.open_page('boochooser');
  // }
  //
  //
  // open_comments(post) {
  //   this.page.comments.post = post;
  //
  //   // 코멘트창이 최초로 열릴때 post정보를 업데이트하는 시간때문에 약간의 딜레이를 준다
  //   setTimeout(() => { this.open_page('comments'); }, 100);
  // }

  // open_booposts() {
  //   this.open_page('booposts');
  // }
  //
  // open_posting_guide() {
  //   if (this.user.auth) {
  //     this.open_bridge('posting_guide', 'bottom');
  //
  //   } else {
  //     this.open_bridge('login_guide_for_posting', 'bottom');
  //   }
  // }
  //
  // open_newpost(type) {
  //   this.close_pages_all();
  //   this.page.posting.post = undefined;
  //   this.page.posting.type = type;
  //   this.open_page('posting');
  // }
  //
  // open_editpost(post) {
  //   this.page.posting.post = post;
  //   this.page.posting.type = undefined;
  //   this.open_page('posting');
  // }
  //
  //
  // open_infoboard(position) {
  //   this.page.infoboard.contents = position;
  //   this.open_page('infoboard');
  // }
  //
  //
  // open_boopage(boo) {
  //   if (this.mode.on=='posting') {
  //     return
  //
  //   // } else if (this.auth && this.auth.boo_selected==boo.id) {
  //   } else if (this.user.is_myboo(boo)) {
  //     this.open_mypage();
  //
  //   } else if (this.mode.on=='booposts') {
  //     this.close_page();
  //
  //   } else if (this.user.guest.boo.id==boo.id) {
  //     alert('익명사용자입니다');
  //     return
  //
  //   } else if (!boo.active) {
  //     alert('삭제된 사용자입니다');
  //     return
  //
  //   } else {
  //     if (!this.page.boopage.boo || this.page.boopage.boo.id!=boo.id) {
  //       this.page.boopage.boo = boo;
  //     }
  //
  //     this.close_pages_all();
  //     this.open_page('boopage');
  //   }
  // }
  //
  // open_navigator() {
  //   this.close_pages_all();
  //   this.open_page('navigator');
  // }
  //
  // open_home() {
  //   this.close_pages_all();
  //   this.open_page('home');
  // }
  //
  // open_searcher() {
  //   this.open_page('searcher');
  // }
  //
  // open_network(type, boos_group) {
  //   this.page.network.type = type;
  //   this.page.network.boos_group = boos_group;
  //   this.open_page('network');
  // }

}


class Loader {
  constructor(id, store) {
    this.id = id;
    this.store = store;
    this.onloading = true;
  }

  load() {
    fetch(this.url(this.id))
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          Object.assign(this, js.content);
        }
      });
  }
}

class Pix extends Loader {
  constructor(id, store) {
    if (id in store.pixstore) {
      return store.pixstore[id]

    } else {
      super(id, store);
      store.pixstore[this.id] = this;
      this.url = (id) => `/pix/${id}`;
      this.desc = undefined;
      this.src = undefined;
      this.owner = undefined;
      this.outlink = undefined;
      this.load();
    }
  }

  // load() {
  //   fetch(this.url(this.id))
  //     .then(x => x.json())
  //     .then(js => {
  //       this.onloading = false;
  //
  //       if (js.success) {
  //         this.desc = js.content.desc;
  //         this.src = js.content.src;
  //         this.owner = js.content.owner;
  //         this.outlink = js.content.outlink;
  //       }
  //     });
  // }

  load_owner() {
    this.owner = Boo.rebuild(this.owner, this.store);
    // const nick = this.owner.nick;
    // const collections = this.owner.collections;
    // this.owner = new Boo(this.owner.id, this.store);
    // this.owner.evolute(nick, collections);

    // this.owner.nick = nick;
    // this.owner.collectionize(collections);
    // this.owner.collections = collections.map(col => {
    //   return {
    //     id: col.id,
    //     name: col.name,
    //     picks: new Picks(this.store, col.id)
    //   }
    // });

    // if (!this.owner.collections) {
    //   // collections = collections.map(...) 으로 하면 안된다
    //   // 새로운 객체 new Picks(...)에 Vue가 reactive하지 못하다
    //   collections.forEach(col => {
    //     if (!col.picks)
    //       Vue.set(col, 'picks', new Picks(this.store, col.id));
    //   });
    //
    //   this.owner.collections = collections;
    // }
  }
}

class Boo extends Loader {
  constructor(id, store) {
    if (id in store.boostore) {
      return store.boostore[id]

    } else {
      super(id, store);
      store.boostore[this.id] = this;
      this.url = (id) => `/boo/${id}/baseboo`;
      this.text = undefined;
      this.profile = undefined;
      this.active = undefined;
      this.voting_record = undefined;
      this.genderlabels = [];
      this.agelabels = [];
      this.stylelabels = [];
      this.itemlabels = [];
      this.load();
    }
  }

  static rebuild(baseboo, store) {
    const nick = baseboo.nick;
    const collections = baseboo.collections;
    const _boo = new Boo(baseboo.id, store);
    _boo.evolute(nick, collections);
    return _boo
  }

  // load() {
  //   fetch(this.url(this.id))
  //     .then(x => x.json())
  //     .then(js => {
  //       this.onloading = false;
  //
  //       if (js.success) {
  //         Object.assign(this, js.content);
  //       }
  //     });
  // }

  evolute(nick, collections) {
    if (!this.nick) {
      this.nick = nick;
    }

    if (!this.collections) {
      // collections = collections.map(...) 으로 하면 안된다
      // 새로운 객체 new Picks(...)에 Vue가 reactive하지 못하다
      // collections.forEach(col => {
      //   if (!col.picks)
      //     Vue.set(col, 'picks', new Picks(this.store, col.id));
      // });
      //
      // this.collections = collections;
      this.collections = collections.map(col => {
        if (!col.picks) {
          const _col = new Collection(col.id, this.store);
          _col.name = col.name;
          return _col

        } else {
          return col
        }
      })
    }
  }

  has_pix(pix_id, collection) {
    if (collection) {
      if (collection.pixids) {
        return collection.pixids.includes(pix_id)
      }
      return false

    } else if (this.collections) {
      return _.findIndex(this.collections, function(o) {
        if (o.pixids) {
          return o.pixids.includes(pix_id)
        }
        return false
      }) > -1;
    }
  }
}


class Collection extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/collection/${id}`;
    // this.url = (id) => `/collection/${id}/ipixs`;
    this.pixids = undefined;
    this.picks = new Picks(this.store, id);
    this.load();
  }

  // load() {
  //   fetch(this.url(this.id))
  //     .then(x => x.json())
  //     .then(js => {
  //       this.onloading = false;
  //
  //       if (js.success) {
  //         Object.assign(this, js.content);
  //       }
  //     });
  // }
}

class Pick extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/pick/${id}`;
    this.pix = undefined;
    this.load();
  }

  load() {
    fetch(this.url(this.id))
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          this.pix = new Pix(js.content.pix.id, this.store);
        }
      });
  }
}


class Post extends Loader {
  constructor(id, store) {
    super(id, store);
    this.url = (id) => `/post/${id}`;
    this.group = undefined;
    this.load();
  }

  // load() {
  //   fetch(this.url(this.id))
  //     .then(x => x.json())
  //     .then(js => {
  //       this.onloading = false;
  //
  //       if (js.success) {
  //         Object.assign(this, js.content);
  //       }
  //     });
  // }
}


class Multiloader {
  constructor(store) {
    this.store = store;
    this.ids = [];
    this.list = [];
    this.onloading = false;
    this.contentype = undefined;

    this.list_onloading = [];
  }

  load(n) {
    if (this.ids.length == 0) {
      return
    }

    if (!n) { var n = 1; }
    n = Math.min(n, this.ids.length);

    this.list_onloading = [];
    let _id;

    for (let i = 0; i < n; i++) {
      _id = this.ids.shift();
      const content = new this.contentype(_id, this.store)

      if (_.findIndex(this.list, ['id', _id]) == -1) {
        this.list.push(content);
        this.list_onloading.push(content);
      }
    };
  }

  load_ids() {
    this.onloading = true;
    fetch(this.ids_url)
      .then(x => x.json())
      .then(js => {
        this.onloading = false;

        if (js.success) {
          this.ids = js.ids;
          this.load(this.nloads_init);
        }
      });
  }
}



class Pixs extends Multiloader {
  constructor(store) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `/pix/ipixs`;
    this.load_ids();
  }
}


class Searchpixs_by_pix extends Multiloader {
  constructor(store, pix_id) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/pix/${pix_id}`;
    this.load_ids();
  }
}


class Searchpixs_by_keyword extends Multiloader {
  constructor(store, keyword) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/keyword/${keyword}`;
    this.load_ids();
  }
}

class Searchpixs_by_collection extends Multiloader {
  constructor(store, collection_id) {
    super(store);
    this.contentype = Pix;
    this.nloads_init = 10;
    this.ids_url = `search/collection/${collection_id}`;
    this.load_ids();
  }
}

class Picks extends Multiloader {
  constructor(store, collection_id) {
    super(store);
    this.contentype = Pick;
    this.nloads_init = 1;

    if (collection_id) {
      this.ids_url = `/collection/${collection_id}/ipicks`;
      this.load_ids();
    }
  }
}

class Collections extends Multiloader {
  constructor(store) {
    super(store);
    this.contentype = Collection;
    this.nloads_init = 2;
    this.ids_url = `/collection/icols`;
    this.load_ids();
  }
}

class Mbti extends Multiloader {
  constructor(store, type) {
    super(store);
    this.contentype = Post;
    this.nloads_init = 20;
    this.ids_url = `/mbti/${type}/iposts`;
    this.load_ids();
  }
}

// class Searchkeywords extends Multiloader {
//   constructor(store, pix_id) {
//     super(store);
//     this.contentype = Pix;
//     this.nloads_init = 10;
//     this.ids_url = `search/pix/${pix_id}`;
//     this.load_ids();
//   }
// }


class Store {
  constructor() {
    this.pixstore = {};
    this.boostore = {};
  }

  // get(id) {
  //   return this.dict[id]
  // }
}

// class Posts extends ContentLoader {
//   constructor(type, ninit) {
//     super();
//     // this.nloads_init = (ninit ? ninit : 24);
//     this.nloads_init = (ninit ? ninit : 12);
//     // this.nloads_init = (ninit ? ninit : 4);
//     this.idlist_url = `/posts/iposts/${type}`;
//     this.content_url = (id) => `/post/${id}`;
//     this.load_idlist();
//   }
// }
//
//
// class SearchPosts extends ContentLoader {
//   constructor(keywords) {
//     super();
//     this.nloads_init = 15;
//     this.idlist_url = `/search/${keywords}`;
//     this.content_url = (id) => `/post/${id}`;
//     this.load_idlist();
//   }
// }
//
//
// class Booposts extends ContentLoader {
//   constructor(boo, type) {
//     super();
//     this.boo = boo;
//     this.nloads_init = 6;
//     // this.nloads_init = 16;
//     this.idlist_url = `/boo/${boo.id}/iposts/${type}`;
//     // this.idlist_url = `/posts/iposts/${boo.id}`;
//     this.content_url = (id) => `/post/${id}/boo`;
//     this.load_idlist();
//   }
// }
//
// class Mbti extends ContentLoader {
//   constructor(type) {
//     super();
//     this.nloads_init = 20;
//     this.idlist_url = `/mbti/${type}/iposts`;
//     this.content_url = (id) => `/post/${id}`;
//     this.load_idlist();
//   }
// }
//
// class Comments extends ContentLoader {
//   constructor(post) {
//     super();
//     this.nloads_init = 10;
//     this.idlist_url = `/post/${post.id}/icomments`;
//     this.content_url = (id) => `/comment/${id}`;
//     this.load_idlist();
//   }
// }
//
// class Voters extends ContentLoader {
//   constructor(post, act) {
//     super();
//     this.nloads_init = 5;
//     this.n_guestboos = 0;
//     this.idlist_url = `/post/${post.id}/ivoters/${act}`;
//     this.content_url = (id) => `/boo/${id}/baseboo`;
//     // this.content_url = (id) => `/boo/${id}/voter`;
//     this.load_idlist();
//   }
// }
//
// class Followers extends ContentLoader {
//   constructor(boo) {
//     super();
//     this.nloads_init = 10;
//     this.idlist_url = `/boo/${boo.id}/ifollowers`;
//     this.content_url = (id) => `/boo/${id}/baseboo`;
//     // this.content_url = (id) => `/boo/${id}/follower`;
//     this.load_idlist();
//   }
// }
//
// class Boos extends ContentLoader {
//   constructor(type) {
//     super();
//     this.nloads_init = 10;
//     this.idlist_url = `/boos/iboos/${type}`;
//     this.content_url = (id) => `/boo/${id}/baseboo`;
//     this.load_idlist();
//   }
// }



class User {
  constructor(session) {
    this.auth = undefined;
    this.guest = undefined;
    this.onloading = true;
    this.session = session;
    this.load();
  }

  load() {
    fetch('/user2')
      .then(x => x.json())
      .then(js => {
        // console.log(js);

        if (js.success) {
          this.auth = new Auth(js.user, this.session.store);
          // this.auth = new Auth(JSON.parse(js.user), this.session.store);

          // if (js.first_visit) {
          //   this.auth.first_visit = js.first_visit;
          //   this.session.open_profiler();
          // }
        }

        this.guest = { boo: JSON.parse(js.guestboo) };
        this.onloading = false;
      });
  }

  get has_auth() {
    return this.auth ? true : false
  }

  get is_guest() {
    return this.guest ? true : false
  }

  get boo() {
    if (this.has_auth) {
      return this.auth.boo

    } else if (this.is_guest){
      return this.guest.boo
    }
  }

  is_myboo(boo) {
    if (this.has_auth) {
      return this.auth.is_myboo(boo)
    }
  }

  is_following(boo) {
    return this.has_auth && !this.is_myboo(boo) && this.auth.is_following(boo.id)
  }

  follow(boo) {
    if (this.has_auth) {
      this.auth.follow(boo.id)
    }
  }

  unfollow(boo) {
    if (this.has_auth) {
      this.auth.unfollow(boo.id)
    }
  }

  get boos_fully_loaded() {
    if (this.has_auth) {
      return this.auth.boos_fully_loaded

    } else {
      return true
    }
  }

  vote(post_id, action) {
    if (!this.boo) {
      return
    }

    const feed_act = {};
    feed_act[post_id] = action;
    this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);

    fetch(`/post/${post_id}/vote?action=${action}`)
      .then(x => x.json())
      .then(js => {
        console.log(js);
        this.boo.fit = js.fit;
      });
  }

  has_voted_as(post_id) {
    if (!this.boo)
      return

    if (post_id in this.boo.voting_record) {
      return this.boo.voting_record[post_id]

    } else {
      return -1
    }
  }

  has_liked_comment(comment_id) {
    if (this.boo)
      return this.boo.ilikes_comment.includes(comment_id)
  }

  like_comment(comment_id) {
    if (this.boo)
      this.boo.ilikes_comment.push(comment_id)
  }

  delike_comment(comment_id) {
    if (this.boo) {
      const where = this.boo.ilikes_comment.indexOf(comment_id);
      this.boo.ilikes_comment.splice(where, 1);
    }
  }
}


class Auth {
  constructor(cuser, store) {
    // console.log(cuser)
    this.id = Number(cuser.id);
    this.store = store;
    this.email = cuser.email;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boo ? {[cuser.boo_selected]: Boo.rebuild(cuser.boo, store)} : {};
    // this.boos = cuser.boo ? {[cuser.boo_selected]: cuser.boo} : {};
    this.boos_fully_loaded = false;
    this.links = cuser.links;
    // this.first_visit = false;
    this.load_other_boos();
  }

  is_myboo(boo) {
    return boo.id == this.boo_selected
  }

  api_get(url) {
    fetch(url)
      .then(x => x.json())
      .then(js => {
        console.log(js)
      });
  }

  load_other_boos() {
    fetch('/user2/other_boos')
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          // this.boos = { ...this.boos, ...JSON.parse(js.other_boos) };
          this.boos = { ...this.boos, ...js.other_boos };
          this.boos_fully_loaded = true;
        }
      })
  }

  set boo(boo_id) {
    if (this.boo) {
      console.log(`boo changed to [${boo_id}]${this.boos[boo_id].nick} from [${this.boo_selected}]${this.boo.nick}`);

    } else {
      console.log(`boo [${boo_id}]${this.boos[boo_id].nick} created at the first time`);
    }

    this.boo_selected = Number(boo_id);
    this.boos[this.boo_selected] = Boo.rebuild(this.boos[this.boo_selected], this.store);
    this.api_get(`/boo/${boo_id}/set/`);
  }

  get boo() {
    return this.boos[this.boo_selected];
  }

  is_following(author_id) {
    return this.boo.followees_id.includes(author_id);
  }

  unfollow(author_id) {
    this.api_get(`/boo/${author_id}/unfollow`);

    const where = this.boo.followees_id.indexOf(author_id);
    this.boo.followees_id.splice(where, 1);
  }

  follow(author_id) {
    this.api_get(`/boo/${author_id}/follow`);
    this.boo.followees_id.push(author_id);
  }

  // has_voted_as(post_id) {
  //   if (post_id in this.boo.voting_record) {
  //     return this.boo.voting_record[post_id]
  //
  //   } else {
  //     return -1
  //   }
  // }

  // has_liked_comment(comment_id) {
  //   return this.boo.ilikes_comment.includes(comment_id)
  // }
  //
  // like_comment(comment_id) {
  //   this.boo.ilikes_comment.push(comment_id)
  // }
  //
  // delike_comment(comment_id) {
  //   const where = this.boo.ilikes_comment.indexOf(comment_id);
  //   this.boo.ilikes_comment.splice(where, 1);
  // }

  // vote(post_id, action) {
  //   const feed_act = {};
  //   feed_act[post_id] = action;
  //   this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);
  //
  //   fetch(`/post/${post_id}/vote?action=${action}`)
  //     .then(x => x.json())
  //     .then(js => {
  //       console.log(js);
  //       this.boo.fit = js.fit;
  //     });
  // }
}
