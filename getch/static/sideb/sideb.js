const guestboo = 363;

class Session {
  constructor() {
    this.page = {
      home:       { open: false, from: 'left', hotboos: new Boos('hot') },
      // posts:      { contents: new Posts(), univ: { history: new Posts(), hot: undefined, custom: undefined }, swiper: undefined },
      // posts:      { contents: undefined, univ: { history: new Posts('hot', 4), hot: undefined, custom: undefined, search: undefined }, swiper: undefined },
      posts:      { open: true, contents: undefined, univ: { hot: new Posts('hot'), history: new Posts('history'), custom: undefined, search: undefined }, swiper: undefined },
      mypage:     { open: false, from: 'left' },
      loginpage:  { open: false, from: 'bottom' },
      navigator:  { open: false, from: 'left' },
      profiler:   { open: false, from: 'right', type: undefined },
      boopage:    { open: false, from: 'left', boo: undefined },
      network:    { open: false, from: 'right', type: undefined, boos_group: undefined },
      posting:    { open: false, from: 'right', post: undefined, type: undefined },
      comments:   { open: false, from: 'right', post: undefined },
      booposts:   { open: false, from: 'right', open_at: 0, swiper: undefined },
      pixeditor:  { open: false, src: undefined, pixloader: undefined, type: undefined },
      texteditor: { open: false, basetext: undefined, setter: undefined, placeholder: undefined, maxlines: 1 },
      bridge:     { open: false, from: undefined, type: undefined, callback: undefined, args: undefined },
      searcher:   { open: false, from: 'right' },
      company:    { open: false, from: 'right', section: 'who' },
      landing:    { open: false, from: 'right' },
      infoboard:  { open: false, from: 'right', contents: undefined },
    };

    this.mode = { on: 'posts', order: 0, prev: undefined };
    // this.auth = undefined;
    // this.guest = undefined;
    this.booposts = undefined;
    this.page.posts.contents = this.page.posts.univ.history;

    // this.fetch_user();
    this.user = new User(this);
  }

  // fetch_user() {
  //   fetch('/user')
  //     .then(x => x.json())
  //     .then(js => {
  //       if (js.success) {
  //         this.auth = new Auth(JSON.parse(js.user));
  //
  //         if (js.first_visit) {
  //           this.auth.first_visit = js.first_visit;
  //           this.open_profiler();
  //         }
  //
  //       } else {
  //         this.guest = {
  //           boo: JSON.parse(js.guestboo)
  //         };
  //       }
  //     });
  // }

  logout() {
    this.open_bridge('logout_guide', 'top', () => {
      this.close_page();
      this.expire();

      fetch('/logout/')
        .then(x => {
          if (x.ok) {
            console.log('successfully logged out');
            // this.user = new User(this);
          }
        });
    });
  }

  expire() {
    // auth만 제거하고, guest는 상주하게 한다
    this.user.auth = undefined;
    // this.user.guest = undefined;
  }

  close_page() {
    this.page[this.mode.on].open = false;
    this.checkout();
  }

  close_pages_all() {
    while (this.mode.on!='posts') {
      this.close_page();
    }
  }

  open_page(pagename) {
    this.page[pagename].open = true;
    this.checkin(pagename);
  }

  open_loginpage() {
    this.open_page('loginpage');
  }

  open_mypage() {
    this.close_pages_all();

    if (this.user.auth) {
      this.open_page('mypage');

    } else {
      this.open_bridge('login_guide_for_mypage', 'bottom');
    }
  }

  open_bridge(type, from, callback, args) {
    this.page.bridge.type = type;
    this.page.bridge.from = from;
    this.page.bridge.callback = callback;
    this.page.bridge.args = args;
    this.open_page('bridge');
  }

  open_boochooser() {
    this.open_page('boochooser');
  }

  open_profiler(type) {
    if (type) {
      this.page.profiler.type = type;

    } else {
      this.page.profiler.type = undefined;
    }

    this.open_page('profiler');
  }

  open_comments(post) {
    this.page.comments.post = post;

    // 코멘트창이 최초로 열릴때 post정보를 업데이트하는 시간때문에 약간의 딜레이를 준다
    setTimeout(() => { this.open_page('comments'); }, 100);
  }

  open_booposts() {
    this.open_page('booposts');
  }

  open_posting_guide() {
    if (this.user.auth) {
      this.open_bridge('posting_guide', 'bottom');

    } else {
      this.open_bridge('login_guide_for_posting', 'bottom');
    }
  }

  open_newpost(type) {
    this.close_pages_all();
    this.page.posting.post = undefined;
    this.page.posting.type = type;
    this.open_page('posting');
  }

  open_editpost(post) {
    this.page.posting.post = post;
    this.page.posting.type = undefined;
    this.open_page('posting');
  }

  open_company(section) {
    if (section) {
      this.page.company.section = section;

    } else {
      this.page.company.section = 'who';
    }

    // this.close_pages_all();
    this.open_page('company');
  }

  open_landing() {
    // this.close_pages_all();
    this.open_page('landing');
  }

  open_infoboard(position) {
    this.page.infoboard.contents = position;
    this.open_page('infoboard');
  }


  open_boopage(boo) {
    if (this.mode.on=='posting') {
      return

    // } else if (this.auth && this.auth.boo_selected==boo.id) {
    } else if (this.user.is_myboo(boo)) {
      this.open_mypage();

    } else if (this.mode.on=='booposts') {
      this.close_page();

    } else if (this.user.guest.boo.id==boo.id) {
      alert('익명사용자입니다');
      return

    } else if (!boo.active) {
      alert('삭제된 사용자입니다');
      return

    } else {
      if (!this.page.boopage.boo || this.page.boopage.boo.id!=boo.id) {
        this.page.boopage.boo = boo;
      }

      this.close_pages_all();
      this.open_page('boopage');
    }
  }

  open_pixeditor(src, type, pixloader) {
    this.page.pixeditor.src = src;
    this.page.pixeditor.type = type;
    this.page.pixeditor.pixloader = pixloader;
    this.open_page('pixeditor');
  }

  open_texteditor(basetext, placeholder, maxlines, setter) {
    this.page.texteditor.basetext = basetext;
    this.page.texteditor.placeholder = placeholder;
    this.page.texteditor.setter = setter;
    this.page.texteditor.maxlines = maxlines;
    this.open_page('texteditor');
  }

  open_navigator() {
    this.close_pages_all();
    this.open_page('navigator');
  }

  open_home() {
    this.close_pages_all();
    this.open_page('home');
  }

  open_searcher() {
    this.open_page('searcher');
  }

  open_network(type, boos_group) {
    this.page.network.type = type;
    this.page.network.boos_group = boos_group;
    this.open_page('network');
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

}



class ContentLoader {
  constructor() {
    this.list = [];
    this.idlist = [];
    this.onloading = true;
    this.counter = 0;
  }

  load(n) {
    this.onloading = true;

    if (this.idlist.length == 0) {
      this.onloading = false;
      return
    }

    if (!n) { var n = 1; }
    n = Math.min(n, this.idlist.length);

    // const promises = this.idlist.map(id => this.load_by_id(id));
    const promises = [];
    for (let i = 0; i < n; i++) {
      promises.push(this.load_by_id(this.idlist.shift(), this.counter++));
    };

    Promise.all(promises).then(results => {
      console.log('contents loaded');
      this.onloading = false;
    });
  }

  load_idlist() {
    fetch(this.idlist_url)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          if (this.constructor.name == 'Voters') {
            this.n_guestboos = js.idlist.filter(i => i==guestboo).length;
          }

          this.idlist = js.idlist;
          this.load(this.nloads_init);
        }
      });
  }

  load_by_id(id, order) {
    return fetch(this.content_url(id))
            .then(x => x.json())
            .then(js => {
              if (js.success) {
                js.content.order = order;
                this.list.push(js.content);
              }
            })
  }
}


class Posts extends ContentLoader {
  constructor(type, ninit) {
    super();
    // this.nloads_init = (ninit ? ninit : 24);
    this.nloads_init = (ninit ? ninit : 12);
    // this.nloads_init = (ninit ? ninit : 4);
    this.idlist_url = `/posts/iposts/${type}`;
    this.content_url = (id) => `/post/${id}`;
    this.load_idlist();
  }
}


class SearchPosts extends ContentLoader {
  constructor(keywords) {
    super();
    this.nloads_init = 15;
    this.idlist_url = `/search/${keywords}`;
    this.content_url = (id) => `/post/${id}`;
    this.load_idlist();
  }
}


class Booposts extends ContentLoader {
  constructor(boo, type) {
    super();
    this.boo = boo;
    this.nloads_init = 6;
    // this.nloads_init = 16;
    this.idlist_url = `/boo/${boo.id}/iposts/${type}`;
    // this.idlist_url = `/posts/iposts/${boo.id}`;
    this.content_url = (id) => `/post/${id}/boo`;
    this.load_idlist();
  }
}

class Comments extends ContentLoader {
  constructor(post) {
    super();
    this.nloads_init = 10;
    this.idlist_url = `/post/${post.id}/icomments`;
    this.content_url = (id) => `/comment/${id}`;
    this.load_idlist();
  }
}

class Voters extends ContentLoader {
  constructor(post, act) {
    super();
    this.nloads_init = 5;
    this.n_guestboos = 0;
    this.idlist_url = `/post/${post.id}/ivoters/${act}`;
    this.content_url = (id) => `/boo/${id}/baseboo`;
    // this.content_url = (id) => `/boo/${id}/voter`;
    this.load_idlist();
  }
}

class Followers extends ContentLoader {
  constructor(boo) {
    super();
    this.nloads_init = 10;
    this.idlist_url = `/boo/${boo.id}/ifollowers`;
    this.content_url = (id) => `/boo/${id}/baseboo`;
    // this.content_url = (id) => `/boo/${id}/follower`;
    this.load_idlist();
  }
}

class Boos extends ContentLoader {
  constructor(type) {
    super();
    this.nloads_init = 10;
    this.idlist_url = `/boos/iboos/${type}`;
    this.content_url = (id) => `/boo/${id}/baseboo`;
    this.load_idlist();
  }
}



class User {
  constructor(session) {
    this.auth = undefined;
    this.guest = undefined;
    this.onloading = true;
    this.session = session;
    this.load();
  }

  load() {
    fetch('/user')
      .then(x => x.json())
      .then(js => {
        // console.log(js);

        if (js.success) {
          this.auth = new Auth(JSON.parse(js.user));

          if (js.first_visit) {
            this.auth.first_visit = js.first_visit;
            this.session.open_profiler();
          }
        }

        // } else {
        this.guest = { boo: JSON.parse(js.guestboo) };
        // }

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
  constructor(cuser) {
    this.id = Number(cuser.id);
    this.email = cuser.email;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boo ? {[cuser.boo_selected]: cuser.boo} : {};
    this.boos_fully_loaded = false;
    this.links = cuser.links;
    this.first_visit = false;
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
    fetch('/user/other_boos')
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          this.boos = { ...this.boos, ...JSON.parse(js.other_boos) };
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
