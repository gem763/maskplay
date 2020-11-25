class Session {
  constructor() {
    this.page = {
      posts:      { contents: new Posts(), swiper: undefined },
      mypage:     { open: false, from: 'left' },
      loginpage:  { open: false, from: 'bottom' },
      navigator:  { open: false, from: 'left' },
      boochooser: { open: false, from: 'left' },
      profiler:   { open: false, from: 'right', type: undefined },
      boopage:    { open: false, from: 'left', boo: undefined },
      network:    { open: false, from: 'right' },
      posting:    { open: false, from: 'right', mother: undefined },
      comments:   { open: false, from: 'right', post: undefined },
      booposts:   { open: false, from: 'right', open_at: 0, swiper: undefined },
      pixeditor:  { open: false, src: undefined, pixloader: undefined, type: undefined },
      texteditor: { open: false, basetext: undefined, setter: undefined, placeholder: undefined },
      bridge:     { open: false, from: 'bottom', type: undefined },
    };

    this.mode = { on: 'posts', order: 0, prev: undefined };
    this.auth = undefined;
    // this.posts = new Posts();
    this.posts_open_at = 0;
    this.booposts = undefined;

    this.anonyboo = undefined;
    this.stats = undefined;
    this.styletags = undefined;
    // this.hammer = this.get_hammer();

    this.fetch_user();
  }


  fetch_user() {
    fetch('/user')
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          // 화살표 함수 안에서는 그냥 this를 써도 된다
          this.auth = new Auth(JSON.parse(js.user));
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

    } else {
      this.open_bridge('login_guide_for_mypage')
      // this.open_loginpage();
    }
  }

  open_bridge(type) {
    this.page.bridge.type = type;
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
    this.open_page('comments');
  }

  // open_booposts(posts, where) {
  open_booposts() {
    // this.booposts = posts;
    // this.page.booposts.open_at = where;
    // this.page.booposts.swiper.slideTo(where, 1, false);
    this.open_page('booposts');
  }

  open_posting() {
    this.close_pages_all();
    
    if (this.auth) {
      // this.page.posting.mother = mother;
      this.open_page('posting');

    } else {
      this.open_bridge('login_guide_for_posting');
      // this.open_loginpage();
    }
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
    if (this.auth && this.auth.boo_selected==boo.id) {
      this.open_mypage();

    } else if (this.mode.on=='booposts') {
      this.close_page();

    } else if (this.anonyboo.id==boo.id) {
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

  open_texteditor(basetext, placeholder, setter) {
    this.page.texteditor.basetext = basetext;
    this.page.texteditor.placeholder = placeholder;
    this.page.texteditor.setter = setter;
    this.open_page('texteditor');
  }

  open_navigator() {
    this.close_pages_all();
    this.open_page('navigator');
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


  pscore(boo) {
    return (1*boo.nfollowers + 0.2*boo.nposts) + 10
  }

  get total_pscore() {
    return (1*this.stats.total_nfollowers + 0.2*this.stats.total_nposts) + 10*this.stats.total_nboos
  }

  level(boo) {
    const scaler = 0.1;
    const unit = 0.15 * scaler;
    const _ps = this.pscore(boo) / this.total_pscore;

    switch (true) {
      case (0 <= _ps && _ps < unit):
        return 0
      case (unit <= _ps && _ps < 2*unit):
        return 1
      case (2*unit <= _ps && _ps < 3*unit):
        return 2
      case (3*unit <= _ps && _ps < 4*unit):
        return 3
      case (4*unit <= _ps && _ps < 5*unit):
        return 4
      case (5*unit <= _ps):
        return 5
    }
  }

  barcode(boo) {
    return `/static/materials/icons/barcode_${this.level(boo)}.png`
  }

  levelcolor(boo) {
    switch (this.level(boo)) {
      case (0):
        return 'black'
      case (1):
        return 'rgba(0, 176, 240, 1)'
      case (2):
        return 'rgba(33, 170, 74, 1)'
      case (3):
        return 'rgba(247, 232, 3, 1)'
      case (4):
        return 'rgba(247, 123, 37, 1)'
      case (5):
        return 'rgba(255, 0, 0, 1)'
    }
  }
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
              this.list.push(js.content);
            })
  }
}


class Baseposts extends ContentLoader {
  load_idlist() {
    fetch(this.idlist_url)
      .then(x => x.json())
      .then(js => {
        if (js.success) {
          this.idlist = js.iposts;
          this.load(this.nloads_init);
        }
      });
  }

  load_by_id(id) {
    return fetch(this.post_url(id))
            .then(x => x.json())
            .then(js => {
              this.list.push(js.post);
            })
  }

  // delete_cpost() {
  //   const where = this.swiper.realIndex;
  //   this.swiper.slideTo(where - 1);
  //   this.list.splice(where, 1);
  //   // this.swiper.removeSlide(where);
  // }
  //
  // listin(post) {
  //   let where = _.findIndex(this.list, ['id', post.id]);
  //
  //   if (where==-1) {
  //     this.list.push(post);
  //
  //   } else {
  //     this.list.splice(where, 1, post);
  //   }
  // }
}


class Posts extends ContentLoader {
  constructor() {
    super();
    this.nloads_init = 24;
    this.idlist_url = '/posts/iposts';
    this.content_url = (id) => `/post/${id}`;
    this.load_idlist();
  }
}

class Booposts extends ContentLoader {
  constructor(boo) {
    super();
    this.boo = boo;
    this.nloads_init = 16;
    this.idlist_url = `/posts/iposts/${boo.id}`;
    this.content_url = (id) => `/post/${id}/boo`;
    this.load_idlist();
  }
}

class Comments extends ContentLoader {
  constructor(post) {
    super();
    this.nloads_init = 30;
    this.idlist_url = `/post/${post.id}/icomments`;
    this.content_url = (id) => `/comment/${id}`;
    this.load_idlist();
  }
}

class Voters extends ContentLoader {
  constructor(post, act) {
    super();
    this.nloads_init = 10;
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
    this.boos = {[cuser.boo_selected]: cuser.boo};
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
    console.log(`boo changed to [${boo_id}]${this.boos[boo_id].nick} from [${this.boo_selected}]${this.boo.nick}`);
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
    this.api_get(`boo/${author_id}/unfollow`);
    // this.boo.followees_id.delete(author_id);

    const where = this.boo.followees_id.indexOf(author_id);
    this.boo.followees_id.splice(where, 1);
  }

  follow(author_id) {
    this.api_get(`boo/${author_id}/follow`);
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

  vote(post_id, action) {
    const feed_act = {};
    feed_act[post_id] = action;
    this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);

    this.api_get(`post/${post_id}/vote?action=${action}`);
  }

  new_boo() {
    const self = this;
    return fetch('boo/new/')
      .then(res => res.json())
      .then(js => {
        if (js.success) {
          const boo = JSON.parse(js.boo);
          self.boos[boo.id] = boo;
          self.boo_selected = boo.id;
        }
      })
  }
}
