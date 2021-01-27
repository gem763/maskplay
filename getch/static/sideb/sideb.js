class Session {
  constructor() {
    this.page = {
      // posts:      { contents: new Posts(), univ: { history: new Posts(), hot: undefined, custom: undefined }, swiper: undefined },
      // posts:      { contents: undefined, univ: { history: new Posts('hot', 4), hot: undefined, custom: undefined, search: undefined }, swiper: undefined },
      posts:      { open: true, contents: undefined, univ: { history: new Posts('history'), hot: new Posts('hot'), custom: undefined, search: undefined }, swiper: undefined },
      mypage:     { open: false, from: 'left' },
      loginpage:  { open: false, from: 'bottom' },
      navigator:  { open: false, from: 'left' },
      profiler:   { open: false, from: 'right', type: undefined },
      boopage:    { open: false, from: 'left', boo: undefined },
      network:    { open: false, from: 'right', boos: undefined },
      posting:    { open: false, from: 'right', post: undefined, type: undefined },
      comments:   { open: false, from: 'right', post: undefined },
      booposts:   { open: false, from: 'right', open_at: 0, swiper: undefined },
      pixeditor:  { open: false, src: undefined, pixloader: undefined, type: undefined },
      texteditor: { open: false, basetext: undefined, setter: undefined, placeholder: undefined, maxlines: 1 },
      bridge:     { open: false, from: undefined, type: undefined, callback: undefined },
      searcher:   { open: false, from: 'right' },
      company:    { open: false, from: 'right', section: 'who' },
      infoboard:  { open: false, from: 'right', contents: undefined },
    };

    // this.req = undefined;
    this.mode = { on: 'posts', order: 0, prev: undefined };
    this._auth = undefined;
    // this.posts_open_at = 0;
    this.booposts = undefined;
    // this.hammer = this.get_hammer();

    this.page.posts.contents = this.page.posts.univ.history;
    this.fetch_user();
  }

  get auth() {
    if (this._auth) {
      if (this._auth.boo) {
        return this._auth
      }
    }
  }


  fetch_user() {
    fetch('/user')
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          // console.log(js)
          // 화살표 함수 안에서는 그냥 this를 써도 된다
          this._auth = new Auth(JSON.parse(js.user));

          if (!this._auth.boo) {
            this.open_profiler('new');
          }
        }
      });
  }


  // get_hammer() {
  //   const self = this;
  //   const hammer = new Hammer(document);
  //
  //   function getStartX(e) {
  //     const delta_x = e.deltaX;
  //     const final_x = e.srcEvent.pageX || e.srcEvent.screenX || 0;
  //     const canvas_w = document.querySelector('#window').offsetWidth;
  //     return (final_x - delta_x) / canvas_w;
  //   }
  //
  //   hammer.on('swiperight swipeleft', function (e) {
  //     e.preventDefault();
  //     const x = getStartX(e);
  //
  //     if (self.mode.on == 'journey') {
  //       if (e.type=='swiperight') {
  //         self.open_boochooser();
  //
  //       } else if (e.type=='swipeleft') {
  //         self.open_boopage(self.cpost.boo);
  //       }
  //
  //     } else {
  //       if (e.type=='swiperight' && self.page[self.mode.on].from=='right') {
  //         self.close_page();
  //
  //       } else if (e.type=='swipeleft' && self.page[self.mode.on].from=='left') {
  //         self.close_page();
  //       }
  //     }
  //   });
  //
  //   return hammer
  // }

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

    if (this.auth) {
      this.open_page('mypage');

    } else if (this._auth) {
      this.open_profiler('new');

    } else {
      this.open_bridge('login_guide_for_mypage', 'bottom');
      // this.open_loginpage();
    }
  }

  open_bridge(type, from, callback) {
    this.page.bridge.type = type;
    this.page.bridge.from = from;
    this.page.bridge.callback = callback;
    this.open_page('bridge');
  }

  open_boochooser() {
    this.open_page('boochooser');
  }

  open_profiler(type) {
    // this.page.profiler.key = undefined;
    if (type) {
      this.page.profiler.type = type;

    } else {
      this.page.profiler.type = undefined;
    }

    this.open_page('profiler');
  }

  // open_newprofiler(bookey) {
  //   this.page.profiler.key = bookey;
  //   this.open_page('profiler');
  // }

  open_comments(post) {
    this.page.comments.post = post;

    // 코멘트창이 최초로 열릴때 post정보를 업데이트하는 시간때문에 약간의 딜레이를 준다
    setTimeout(() => { this.open_page('comments'); }, 100);
    // this.open_page('comments');
  }

  // open_booposts(posts, where) {
  open_booposts() {
    // this.booposts = posts;
    // this.page.booposts.open_at = where;
    // this.page.booposts.swiper.slideTo(where, 1, false);
    this.open_page('booposts');
  }

  // open_posting() {
  open_posting_guide() {
    // this.close_pages_all();

    if (this.auth) {
      this.open_bridge('posting_guide', 'bottom');
      // this.open_page('posting');

    } else if (this._auth) {
      this.open_profiler('new');

    } else {
      this.open_bridge('login_guide_for_posting', 'bottom');
    }
  }

  // open_posting(type) {
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

    this.close_pages_all();
    this.open_page('company');
  }

  open_infoboard(position) {
    this.page.infoboard.contents = position;
    this.open_page('infoboard');
  }

  // open_posting(mother) {
  //   if (this.auth) {
  //     this.page.posting.mother = mother;
  //     this.open_page('posting');
  //   } else {
  //     this.open_loginpage();
  //   }
  // }


  open_boopage(boo) {
    if (this.mode.on=='posting') {
      return

    } else if (this.auth && this.auth.boo_selected==boo.id) {
      this.open_mypage();

    } else if (this.mode.on=='booposts') {
      this.close_page();

    // } else if (this.anonyboo.id==boo.id) {
    //   alert('삭제된 사용자입니다');

    } else if (!boo.active) {
      alert('삭제된 사용자입니다');

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

  open_searcher() {
    this.open_page('searcher');
  }

  open_network(boos) {
    this.page.network.boos = boos;
    this.open_page('network');
  }

  // open_network() {
  //   if (this.mode.on=='mypage') {
  //     this.cnetwork.boo = this.auth.boo;
  //   } else if (this.mode.on=='authorpage') {
  //     this.cnetwork.boo = this.cpost.boo;
  //   }
  //
  //   this.cnetwork.followers = undefined;
  //   this.cnetwork.followees = undefined;
  //
  //   self = this;
  //   fetch(`/boo/${self.cnetwork.boo.id}/network/`)
  //     .then(x => x.json())
  //     .then(js => {
  //       const _network = JSON.parse(js.network);
  //       console.log(_network);
  //       self.cnetwork.followers = _network.followers;
  //       self.cnetwork.followees = _network.followees;
  //     })
  //
  //   this.open_page('network');
  // }

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


  // pscore(boo) {
  //   return (1*boo.nfollowers + 0.2*boo.nposts) + 10
  // }
  //
  // get total_pscore() {
  //   return (1*this.stats.total_nfollowers + 0.2*this.stats.total_nposts) + 10*this.stats.total_nboos
  // }
  //
  // level(boo) {
  //   const scaler = 0.1;
  //   const unit = 0.15 * scaler;
  //   const _ps = this.pscore(boo) / this.total_pscore;
  //
  //   switch (true) {
  //     case (0 <= _ps && _ps < unit):
  //       return 0
  //     case (unit <= _ps && _ps < 2*unit):
  //       return 1
  //     case (2*unit <= _ps && _ps < 3*unit):
  //       return 2
  //     case (3*unit <= _ps && _ps < 4*unit):
  //       return 3
  //     case (4*unit <= _ps && _ps < 5*unit):
  //       return 4
  //     case (5*unit <= _ps):
  //       return 5
  //   }
  // }

  // barcode(boo) {
  //   return `/static/materials/icons/barcode_${this.level(boo)}.png`
  // }
  //
  // levelcolor(boo) {
  //   switch (this.level(boo)) {
  //     case (0):
  //       return 'black'
  //     case (1):
  //       return 'rgba(0, 176, 240, 1)'
  //     case (2):
  //       return 'rgba(33, 170, 74, 1)'
  //     case (3):
  //       return 'rgba(247, 232, 3, 1)'
  //     case (4):
  //       return 'rgba(247, 123, 37, 1)'
  //     case (5):
  //       return 'rgba(255, 0, 0, 1)'
  //   }
  // }
}



class ContentLoader {
  constructor() {
    this.list = [];
    this.idlist = [];
    this.onloading = true;
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
      promises.push(this.load_by_id(this.idlist.shift()));
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
          this.idlist = js.idlist;
          this.load(this.nloads_init);
        }
      });
  }

  load_by_id(id) {
    return fetch(this.content_url(id))
            .then(x => x.json())
            .then(js => {
              if (js.success) {
                this.list.push(js.content);
              }
            })
  }
}


// class Baseposts extends ContentLoader {
//   load_idlist() {
//     fetch(this.idlist_url)
//       .then(x => x.json())
//       .then(js => {
//         if (js.success) {
//           this.idlist = js.iposts;
//           this.load(this.nloads_init);
//         }
//       });
//   }
//
//   load_by_id(id) {
//     return fetch(this.post_url(id))
//             .then(x => x.json())
//             .then(js => {
//               this.list.push(js.post);
//             })
//   }
// }


class Posts extends ContentLoader {
  constructor(type, ninit) {
    super();
    this.nloads_init = (ninit ? ninit : 24);
    // this.nloads_init = (ninit ? ninit : 12);
    // this.nloads_init = (ninit ? ninit : 4);
    this.idlist_url = `/posts/iposts/${type}`;
    this.content_url = (id) => `/post/${id}`;
    this.load_idlist();
  }
}


class SearchPosts extends ContentLoader {
  constructor(keywords) {
    super();
    this.nloads_init = 20;
    this.idlist_url = `/search/${keywords}`;
    this.content_url = (id) => `/post/${id}`;
    this.load_idlist();
  }
}


class Booposts extends ContentLoader {
  constructor(boo, type) {
    super();
    this.boo = boo;
    this.nloads_init = 16;
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
    this.idlist_url = `/post/${post.id}/ivoters/${act}`;
    this.content_url = (id) => `/boo/${id}/voter`;
    this.load_idlist();
  }
}




class Auth {
  constructor(cuser) {
    this.id = Number(cuser.id);
    this.email = cuser.email;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boo ? {[cuser.boo_selected]: cuser.boo} : {};
    this.boos_fully_loaded = false;
    this.load_other_boos();
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

  // get nfollowers() {
  //   return this.boo.followers_id.length;//size;
  // }
  //
  // get nfollowees() {
  //   return this.boo.followees_id.length;//size;
  // }

  is_following(author_id) {
    return this.boo.followees_id.includes(author_id);
    // return this.boo.followees_id.has(author_id);
  }

  unfollow(author_id) {
    this.api_get(`/boo/${author_id}/unfollow`);
    // this.boo.followees_id.delete(author_id);

    const where = this.boo.followees_id.indexOf(author_id);
    this.boo.followees_id.splice(where, 1);
  }

  follow(author_id) {
    this.api_get(`/boo/${author_id}/follow`);
    this.boo.followees_id.push(author_id);
    // this.boo.followees_id.add(author_id);
  }

  // has_voted_to(post_id) {
  //   return (post_id in this.boo.voting_record)
  // }

  has_voted_as(post_id) {
    if (post_id in this.boo.voting_record) {
      return this.boo.voting_record[post_id]

    } else {
      return -1
    }
  }

  has_liked_comment(comment_id) {
    return this.boo.ilikes_comment.includes(comment_id)
  }

  like_comment(comment_id) {
    this.boo.ilikes_comment.push(comment_id)
  }

  delike_comment(comment_id) {
    const where = this.boo.ilikes_comment.indexOf(comment_id);
    this.boo.ilikes_comment.splice(where, 1);
  }

  vote(post_id, action) {
    const feed_act = {};
    feed_act[post_id] = action;
    this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);

    // this.api_get(`/post/${post_id}/vote?action=${action}`);

    fetch(`/post/${post_id}/vote?action=${action}`)
      .then(x => x.json())
      .then(js => {
        console.log(js);
        this.boo.fit = js.fit;
      });
  }

  // new_boo() {
  //   const self = this;
  //   return fetch('boo/new/')
  //     .then(res => res.json())
  //     .then(js => {
  //       if (js.success) {
  //         const boo = JSON.parse(js.boo);
  //         self.boos[boo.id] = boo;
  //         self.boo_selected = boo.id;
  //       }
  //     })
  // }
}
