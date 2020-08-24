class Session {
  constructor() {
    this.open = {
      mypage: false,
      loginpage: false,
      boochooser: false,
      profiler: false,
      authorpage: false,
      network: false,
      posting: false,
    };

    this.mode = { on:'journey', prev:undefined };
    // this.cpost = undefined;
    this.cnetwork = { boo:undefined, followers:undefined, followees:undefined };
    this.auth = undefined;
    this.swiper = undefined;
    this.posts = undefined;
  }

  close_page() {
    this.open[this.mode.on] = false;
    this.checkout();
  }

  open_page(pagename) {
    this.open[pagename] = true;
    this.checkin(pagename);
  }

  open_loginpage() {
    this.open_page('loginpage');
  }

  open_mypage() {
    if (this.auth) {
      this.open_page('mypage');
    } else {
      this.open_loginpage();
    }
  }

  open_boochooser() {
    this.open_page('boochooser');
  }

  open_profiler() {
    this.open_page('profiler');
  }

  open_posting() {
    this.open_page('posting');
  }

  open_authorpage() {
    if (this.auth && this.auth.boo_selected==this.cpost.boo.id) {
      this.open_mypage();

    } else {
      this.open_page('authorpage');
    }
  }

  open_network() {
    if (this.mode.on=='mypage') {
      this.cnetwork.boo = this.auth.boo;
    } else if (this.mode.on=='authorpage') {
      this.cnetwork.boo = this.cpost.boo;
    }

    this.cnetwork.followers = undefined;
    this.cnetwork.followees = undefined;

    self = this;
    fetch(`/boo/${self.cnetwork.boo.id}/network/`)
      .then(x => x.json())
      .then(js => {
        const _network = JSON.parse(js.network);
        console.log(_network);
        self.cnetwork.followers = _network.followers;
        self.cnetwork.followees = _network.followees;
      })

    this.open_page('network');
  }

  checkin(on) {
    console.log(`check-in to ${on}`);
    this.mode.prev = {...this.mode};
    this.mode.on = on;
  }

  checkout() {
    try {
      console.log(`check-out from ${this.mode.on}, back to ${this.mode.prev.on}`)
      this.mode = this.mode.prev;

    } catch(e) {
      console.log('abnormal access')
    }
  }

  // set_cpost(post) {
  //   this.cpost = post;
  // }

  get cpost() {
    if (this.swiper) {
      return this.posts[this.swiper.realIndex]
    }
  }

  push_post(post) {
    const where = this.swiper.realIndex + 1;
    this.posts.splice(where, 0, post);
    this.swiper.slideTo(where);
  }
}


class Auth {
  constructor(cuser) {
    this.id = Number(cuser.id);
    this.email = cuser.email;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = cuser.boos; //this.__init_boos__(cuser.boos);
  }

  // __init_boos__(boos) {
  //   for (let k in boos) {
  //     boos[k].followers_id = new Set(boos[k].followers_id);
  //     boos[k].followees_id = new Set(boos[k].followees_id);
  //   }
  //   return boos
  // }

  api_get(url) {
    fetch(url)
      .then(x => x.json())
      .then(js => {
        console.log(js)
      });
  }


  set boo(boo_id) {
    console.log(`boo changed to [${boo_id}]${this.boos[boo_id].nick} from [${this.boo_selected}]${this.boo.nick}`);
    this.boo_selected = Number(boo_id);
    this.api_get(`/boo/${boo_id}/set/`);
  }

  get boo() {
    return this.boos[this.boo_selected];
  }

  get nfollowers() {
    return this.boo.followers_id.length;//size;
  }

  get nfollowees() {
    return this.boo.followees_id.length;//size;
  }

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
    // if (action==-1) {
    //   delete this.boo.voting_record[post_id];
    //
    // } else {
      const feed_act = {};
      feed_act[post_id] = action;
      this.boo.voting_record = Object.assign({}, this.boo.voting_record, feed_act);
      // this.boo.voting_record[post_id] = action;
    // }

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











class Session_old {
  constructor(cuser) {
    this.mode = {on:'journey', prev:undefined};
    this.id = Number(cuser.id);
    this.email = cuser.email;
    this.boo_selected = Number(cuser.boo_selected);
    this.boos = this._init_boos(cuser.boos);
    this.myboos = Object.keys(cuser.boos).map(Number); //this._init_myboos(cuser.boos);
    this.cpost = {};
  }

  _init_myboos(boos) {
    boos = {...boos};

    for (let k in boos) {
      boos[k].followers_id = new Set(boos[k].followers_id);
      boos[k].followees_id = new Set(boos[k].followees_id);
    }
    return boos
  }

  _init_boos(boos) {
    // boos = {...boos, ...authors};
    // authors = undefined;

    for (let k in boos) {
      boos[k].followers_id = new Set(boos[k].followers_id);
      boos[k].followees_id = new Set(boos[k].followees_id);
    }
    return boos
  }

  api_get(url) {
    fetch(url)
      .then(x => x.json())
      .then(js => {
        console.log(js)
      });
  }

  set vote(action) {
    if (action==-1) {
      delete this.boo.voting_record[this.cpost.post_id];

    } else {
      this.boo.voting_record[this.cpost.post_id] = action;
    }

    this.api_get(`post/${this.cpost.post_id}/vote?action=${action}`);
  }

  get has_voted() {
    if (this.cpost.post_id in this.boo.voting_record) {
      return true
    } else {
      return false
    }
  }

  checkin(on) {
    console.log(`check-in to ${on}`);
    this.mode.prev = {...this.mode};
    this.mode.on = on;
  }

  checkout() {
    try {
      console.log(`check-out from ${this.mode.on}, back to ${this.mode.prev.on}`)
      this.mode = this.mode.prev;

    } catch(e) {
      console.log('abnormal access')
    }
  }

  refresh() {
    set_post();
    set_mypage();
    set_boochooser();
    set_profiler();
    set_posting();
  }


  set_myprofile(boo) {
    console.log(`profile changed to [${boo.profile.pix}]`);
    // this.boo.profile = profile;
    boo.followers_id = new Set(boo.followers_id);
    boo.followees_id = new Set(boo.followees_id);
    // this.boos[this.boo_selected] = {}//{...this.boos[this.boo_selected], ...boo};
    this.boos[this.boo_selected] = boo;
    // test11 = boo;
    this.refresh();
  }

  set myboo(boo_id) {
    console.log(`boo changed to [${boo_id}]${this.boos[boo_id].nick} from [${this.boo_selected}]${this.boo.nick}`);
    this.boo_selected = Number(boo_id);
    // this.refresh();
    this.api_get(`/boo/${boo_id}/set/`);
  }

  get boo() {
    return this.boos[this.boo_selected];
  }

  get nfollowers() {
    return this.boo.followers_id.size;
  }

  get nfollowees() {
    return this.boo.followees_id.size;
  }

  get is_following() {
    // return this.boo.followees_id.includes(Number(boo_id));
    return this.boo.followees_id.has(this.cpost.author_id);
  }

  get author() {
    return this.boos[this.cpost.author_id];
  }

  get author_nfollowers() {
    return this.author.followers_id.size;
  }

  get author_nfollowees() {
    return this.author.followees_id.size;
  }

  unfollow() {
    const boo_id = this.cpost.author_id;
    this.api_get(`boo/${boo_id}/unfollow`);

    // 내 followees에서 지우기
    this.boo.followees_id.delete(boo_id);

    // author의 followers에서 나를 지우기
    this.author.followers_id.delete(this.boo_selected);
  }

  follow() {
    const boo_id = this.cpost.author_id;
    this.api_get(`boo/${boo_id}/follow`);

    // 내 followees에 추가하기
    this.boo.followees_id.add(boo_id);

    // author의 followers에 나를 추가하기
    this.author.followers_id.add(this.boo_selected);
  }
}
